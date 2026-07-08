"""
Corrected investability engine (v2) addressing peer-review fixes.

Fix M1 (no double-counted chemistry ceiling): the Zhou atlas OAE_efficiency IS realized
atmospheric CO2 per unit alkalinity and ALREADY embeds the ~0.8 carbonate ceiling. So for
OAE the atlas f_kin is the SOLE location-efficiency term; there is no separate eta_yield.

Fix M2 (pathway-specific efficiency): only OAE/DOC use the OAE atlas. Biological (kelp) and
iron fertilization use their own realized-atmospheric-removal efficiency priors (Hurd 2024;
Ward 2025), which are NOT the alkalinity-equilibration efficiency.

Realized creditable fraction of a nominal (design) tonne:
    E = eff * (1 - lambda_LCA) * p_issue
where eff = atlas f_kin (OAE), a pathway prior (kelp/iron), or 1 (physics-exempt DOC/burial).
cost_net = cost_gross / E.  Investable iff cost_net < price.

Also: correlated cost<->LCA priors (shared latent), and a BINARY MRV issuance probability
p_issue (you get revenue or you do not), modeled as an expected-value multiplier here and
reported separately as issuance risk.
"""
import numpy as np

# eff_kind: 'atlas_oae' (location f_kin from atlas), 'pathway' (own eff prior), 'exempt' (=1)
# Physics+cost analysis is CONDITIONAL ON ISSUANCE. The separate near-term binary issuance
# probability (ISSUANCE_NEARTERM) is the dominant current-market gate (research literature/08:
# only Planetary has ever issued; ~0.3% of contracted volume issued as of 2025-26).
METHODS_V2 = {
    "Mineral OAE": dict(cost=(30, 165), lca=(0.03, 0.12), eff_kind="atlas_oae", sensitive=True),
    "Electrochemical OAE": dict(cost=(60, 200), lca=(0.04, 0.15), eff_kind="atlas_oae", sensitive=True),
    "DOC / DIC stripping": dict(cost=(100, 400), lca=(0.08, 0.30), eff_kind="exempt", sensitive=False),
    "Marine biomass sinking": dict(cost=(400, 3000), lca=(0.15, 0.50), eff=(0.05, 0.40),
                                   eff_kind="pathway", sensitive=True),   # kelp ~25% central (lit/08)
    "Terrestrial burial (control)": dict(cost=(14, 120), lca=(0.02, 0.08), eff_kind="exempt", sensitive=False),
    "Iron fertilization": dict(cost=(100, 2000), lca=(0.05, 0.15), eff=(0.005, 0.05),
                               eff_kind="pathway", sensitive=True),        # OIF ~2% central (lit/08)
}

# Near-term BINARY probability that a project actually gets credits issued (research literature/08).
ISSUANCE_NEARTERM = {
    "Mineral OAE": (0.05, 0.15), "Electrochemical OAE": (0.03, 0.12),
    "DOC / DIC stripping": (0.01, 0.05), "Marine biomass sinking": (0.002, 0.02),
    "Terrestrial burial (control)": (0.05, 0.25), "Iron fertilization": (0.001, 0.02),
}


def _ln(lo, hi, z):
    """Lognormal draw from 10/90 range using a supplied standard-normal z (for correlation)."""
    mu = (np.log(lo) + np.log(hi)) / 2.0
    sigma = (np.log(hi) - np.log(lo)) / (2.0 * 1.2816)
    return np.exp(mu + sigma * z)


def sample_priors(name, n, rng, rho=0.5):
    """MC-sample correlated cost<->LCA (and pathway eff). CONDITIONAL ON ISSUANCE (no p_issue here)."""
    m = METHODS_V2[name]
    z = rng.standard_normal(n)                       # shared latent
    zc = rho * z + np.sqrt(1 - rho**2) * rng.standard_normal(n)
    zl = rho * z + np.sqrt(1 - rho**2) * rng.standard_normal(n)
    out = {"cost": _ln(*m["cost"], zc),
           "lca": np.clip(_ln(*m["lca"], zl), 0.0, 0.9),
           "eff_kind": m["eff_kind"], "sensitive": m["sensitive"]}
    if m["eff_kind"] == "pathway":
        out["eff"] = np.clip(_ln(*m["eff"], rng.standard_normal(n)), 0.001, 0.95)
    return out


def sample_issuance(name, n, rng):
    lo, hi = ISSUANCE_NEARTERM[name]
    return np.clip(_ln(lo, hi, rng.standard_normal(n)), 0.0005, 0.6)


def realized_fraction(s, f_kin=None):
    """E = eff * (1-lca), conditional on issuance. f_kin required for atlas_oae methods."""
    if s["eff_kind"] == "atlas_oae":
        eff = np.asarray(f_kin)
    elif s["eff_kind"] == "pathway":
        eff = s["eff"]
    else:                                            # exempt
        eff = 1.0
    return eff * (1.0 - s["lca"])


def net_cost(s, f_kin=None):
    return s["cost"] / np.maximum(realized_fraction(s, f_kin), 1e-6)


def p_investable(name, price, n, rng, f_kin_samples=None):
    s = sample_priors(name, n, rng)
    if s["eff_kind"] == "atlas_oae":
        fk = rng.choice(np.asarray(f_kin_samples), size=n) if f_kin_samples is not None else 0.6
    else:
        fk = None
    return float(np.mean(net_cost(s, fk) < price))


def breakeven_fkin(name, price, n, rng):
    """For atlas_oae methods: distribution of the atlas f_kin needed so cost_net<price.
    Returns (median, p10, p90) of required f_kin; np.nan where >1 (never)."""
    s = sample_priors(name, n, rng)
    req = s["cost"] / (price * (1.0 - s["lca"]))   # required atlas f_kin (conditional on issuance)
    req = np.where(req > 1.0, np.nan, req)
    return (float(np.nanmedian(req)) if np.isfinite(req).any() else np.nan,
            float(np.nanpercentile(req, 10)) if np.isfinite(req).any() else np.nan,
            float(np.nanpercentile(req, 90)) if np.isfinite(req).any() else np.nan)
