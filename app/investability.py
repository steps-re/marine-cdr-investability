"""
Reduced-form Monte-Carlo investability engine for marine CDR.

Investability identity (screening, not bankable TEA):
    cost_net = cost_gross / ( f_kin_eff * yield_chem * (1 - lambda_LCA) * nu_MRV )
where
    f_kin_eff  = location air-sea equilibration efficiency (physics) for physics-SENSITIVE
                 methods; = 1 for physics-INSENSITIVE methods (DOC/DIC stripping, terrestrial
                 burial) which remove/store carbon directly.
    yield_chem = chemistry/biology ceiling (mol CO2 per unit intervention, etc.)
    lambda_LCA = fraction of gross removal lost to lifecycle emissions (energy/materials/transport)
    nu_MRV     = fraction of net removal that survives the verification/crediting haircut

A method is investable at a location if cost_net < market credit price P.
The PHYSICS BREAKEVEN is the minimum f_kin at which P(investable) crosses 0.5.

All priors are literature-anchored (see literature/05_techno_economic_priors.md); this is a
first-order screen with wide bands, NOT a bankable techno-economic analysis.
"""
import numpy as np


def _lognorm_from_range(lo, hi, n, rng, clip=None):
    """Sample lognormal with 10th/90th pctiles at lo/hi."""
    mu = (np.log(lo) + np.log(hi)) / 2.0
    sigma = (np.log(hi) - np.log(lo)) / (2.0 * 1.2816)
    x = rng.lognormal(mu, sigma, n)
    if clip is not None:
        x = np.clip(x, clip[0], clip[1])
    return x


# Method archetypes. Ranges are (10th, 90th) percentile priors, at-scale.
#   cost   : $/nominal-tonne CO2 (gross capture-intent cost, before f_kin discount)
#   lca    : lambda_LCA fraction lost to lifecycle emissions
#   mrv    : nu_MRV fraction surviving the verification haircut
#   yield  : chemistry/biology ceiling (point)
#   sensitive : does net cost depend on location air-sea f_kin?
METHODS = {
    "Mineral OAE": dict(
        cost=(30, 165), lca=(0.03, 0.12), mrv=(0.60, 0.85), yield_chem=0.80,
        sensitive=True, label="Mineral OAE (olivine/basalt)"),
    "Electrochemical OAE": dict(
        cost=(60, 200), lca=(0.04, 0.15), mrv=(0.78, 0.90), yield_chem=0.80,
        sensitive=True, label="Electrochemical OAE (Ebb, Planetary)"),
    "DOC / DIC stripping": dict(
        cost=(100, 400), lca=(0.08, 0.30), mrv=(0.88, 0.97), yield_chem=1.00,
        sensitive=False, label="Direct Ocean Capture (Captura, Equatic)"),
    "Marine biomass sinking": dict(
        cost=(400, 3000), lca=(0.15, 0.50), mrv=(0.30, 0.60), yield_chem=0.55,
        sensitive=True, label="Marine biomass sinking (kelp)"),
    "Terrestrial burial (control)": dict(
        cost=(14, 120), lca=(0.02, 0.08), mrv=(0.80, 0.95), yield_chem=1.00,
        sensitive=False, label="Terrestrial biomass burial (control)"),
    "Iron fertilization": dict(
        cost=(100, 2000), lca=(0.05, 0.15), mrv=(0.20, 0.45), yield_chem=0.50,
        sensitive=True, label="Iron fertilization"),
}

N_MC_DEFAULT = 20000


def sample_method(name, n=N_MC_DEFAULT, rng=None, overrides=None):
    """Return dict of MC-sampled parameter arrays for a method.

    `overrides` (optional dict) lets a user replace any prior for this run without editing
    the code: e.g. overrides={"cost": (25, 120), "lca": (0.02, 0.06)} to model an innovation
    that lowers cost and lifecycle emissions. Any key in the METHODS entry can be overridden
    (cost, lca, mrv, yield_chem). This is what powers the Screener's in-browser editor.
    """
    rng = rng or np.random.default_rng(0)
    m = {**METHODS[name], **(overrides or {})}
    return {
        "cost": _lognorm_from_range(*m["cost"], n, rng),
        "lca": _lognorm_from_range(*m["lca"], n, rng, clip=(0.0, 0.9)),
        "mrv": _lognorm_from_range(*m["mrv"], n, rng, clip=(0.02, 0.99)),
        "yield_chem": m["yield_chem"],
        "sensitive": m["sensitive"],
    }


def net_cost(sample, f_kin):
    """Net $/creditable-tonne given a scalar or array f_kin. Physics-insensitive -> f_kin=1."""
    fk = 1.0 if not sample["sensitive"] else np.asarray(f_kin)
    denom = fk * sample["yield_chem"] * (1.0 - sample["lca"]) * sample["mrv"]
    return sample["cost"] / denom


def physics_breakeven(name, price, n=N_MC_DEFAULT, rng=None, grid=None, overrides=None):
    """
    Minimum f_kin at which P(net_cost < price) >= 0.5.
    Returns (breakeven_fkin or np.nan if never/always, f_kin_grid, p_investable_grid).
    For physics-insensitive methods, breakeven is 0 if median cost < price, else nan.
    `overrides` forwards user-edited priors (see sample_method).
    """
    rng = rng or np.random.default_rng(1)
    s = sample_method(name, n, rng, overrides=overrides)
    grid = np.linspace(0.02, 1.0, 50) if grid is None else grid
    if not s["sensitive"]:
        p_inv = np.full_like(grid, float(np.mean(net_cost(s, 1.0) < price)))
        be = 0.0 if p_inv[0] >= 0.5 else np.nan
        return be, grid, p_inv
    p_inv = np.array([np.mean(net_cost(s, fk) < price) for fk in grid])
    idx = np.where(p_inv >= 0.5)[0]
    be = float(grid[idx[0]]) if len(idx) else np.nan
    return be, grid, p_inv


def prob_investable(name, f_kin_samples, price, n=N_MC_DEFAULT, rng=None):
    """P(investable) marginalizing over BOTH method priors and a location f_kin distribution."""
    rng = rng or np.random.default_rng(2)
    s = sample_method(name, n, rng)
    fk = 1.0 if not s["sensitive"] else rng.choice(np.asarray(f_kin_samples), size=n)
    return float(np.mean(net_cost(s, fk) < price))
