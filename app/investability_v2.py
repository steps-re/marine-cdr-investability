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

# All editable per-method assumptions (cost, LCA penalty, efficiency, issuance) now live in
# priors.py — a single documented assumption sheet meant to be edited by outside users
# (e.g. a company plugging in an innovation that changes energy/LCA/cost). This module is the
# math; priors.py is the numbers. See priors.py for units, provenance, and a worked example.
try:
    from .priors import METHODS_V2, ISSUANCE_NEARTERM        # package import
except ImportError:
    from priors import METHODS_V2, ISSUANCE_NEARTERM         # flat/script import


def _ln(lo, hi, z):
    """Lognormal draw from 10/90 range using a supplied standard-normal z (for correlation)."""
    mu = (np.log(lo) + np.log(hi)) / 2.0
    sigma = (np.log(hi) - np.log(lo)) / (2.0 * 1.2816)
    return np.exp(mu + sigma * z)


def sample_priors(name, n, rng, rho=0.5, overrides=None):
    """MC-sample correlated cost<->LCA (and pathway eff). CONDITIONAL ON ISSUANCE (no p_issue here).

    `overrides` (optional dict) replaces any prior for this run without editing the code:
    e.g. overrides={"cost": (25, 120), "lca": (0.02, 0.06)}. Powers the Screener's editor.
    """
    m = {**METHODS_V2[name], **(overrides or {})}
    z = rng.standard_normal(n)                       # shared latent
    zc = rho * z + np.sqrt(1 - rho**2) * rng.standard_normal(n)
    zl = rho * z + np.sqrt(1 - rho**2) * rng.standard_normal(n)
    out = {"cost": _ln(*m["cost"], zc),
           "lca": np.clip(_ln(*m["lca"], zl), 0.0, 0.9),
           "eff_kind": m["eff_kind"], "sensitive": m["sensitive"]}
    if m["eff_kind"] == "pathway":
        out["eff"] = np.clip(_ln(*m["eff"], rng.standard_normal(n)), 0.001, 0.95)
    return out


def sample_issuance(name, n, rng, overrides=None):
    lo, hi = (overrides or {}).get("issuance", ISSUANCE_NEARTERM[name])
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


def p_investable(name, price, n, rng, f_kin_samples=None, overrides=None):
    s = sample_priors(name, n, rng, overrides=overrides)
    if s["eff_kind"] == "atlas_oae":
        fk = rng.choice(np.asarray(f_kin_samples), size=n) if f_kin_samples is not None else 0.6
    else:
        fk = None
    return float(np.mean(net_cost(s, fk) < price))


def breakeven_fkin(name, price, n, rng, overrides=None):
    """For atlas_oae methods: distribution of the atlas f_kin needed so cost_net<price.
    Returns (median, p10, p90) of required f_kin; np.nan where >1 (never)."""
    s = sample_priors(name, n, rng, overrides=overrides)
    req = s["cost"] / (price * (1.0 - s["lca"]))   # required atlas f_kin (conditional on issuance)
    req = np.where(req > 1.0, np.nan, req)
    return (float(np.nanmedian(req)) if np.isfinite(req).any() else np.nan,
            float(np.nanpercentile(req, 10)) if np.isfinite(req).any() else np.nan,
            float(np.nanpercentile(req, 90)) if np.isfinite(req).any() else np.nan)
