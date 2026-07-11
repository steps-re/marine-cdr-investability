"""
priors.py — the editable assumption sheet for the marine-CDR investability model.
====================================================================================

This file is the ONE place to change what the model believes about each carbon-removal
method. It is written to be edited by non-authors: a company, an analyst, or a reviewer
who thinks a number should be different can change it here and re-run, with no other code
touched. Every number has a plain-English meaning, a unit, and a source.

--------------------------------------------------------------------------------
THE MODEL, IN ONE LINE
--------------------------------------------------------------------------------
A "nominal tonne" is what a project is designed to remove. What actually gets credited is

    realized_fraction  =  efficiency  x  (1 - lca_penalty)          [conditional on issuance]
    net_cost           =  gross_cost / realized_fraction            [USD per creditable tonne]
    a project is "investable" at a carbon price P  iff  net_cost < P

and, separately, near-term issuance probability (does anyone actually pay you yet) is the
dominant real-world gate today. The three levers a company controls are therefore:

    1. gross_cost      — USD per nominal tonne (capex + opex, at scale)
    2. lca_penalty     — the fraction of the removal eaten by lifecycle emissions
                         (energy, materials, transport, process). See LCA_NOTES below.
    3. efficiency      — how much of the nominal tonne is really removed from the atmosphere:
                           * 'atlas_oae'  -> taken from the Zhou 2024 ocean-efficiency atlas
                                             at the deployment lat/lon (NOT set here)
                           * 'pathway'    -> a method-specific realized-removal fraction (set here)
                           * 'exempt'     -> 1.0 (physics-exempt: DOC, terrestrial burial)

Ranges are 10th–90th-percentile priors, sampled lognormally in the Monte Carlo. cost and
lca share a latent factor (rho, energy-intensive -> both higher).

--------------------------------------------------------------------------------
HOW TO CUSTOMIZE (worked example)
--------------------------------------------------------------------------------
Say your company has a mineral-OAE grinding innovation that cuts grinding energy in half.
Grinding energy is the dominant driver of both the cost and the LCA penalty for Mineral OAE
(see Appendix B.1 of the paper). You would:

    METHODS["Mineral OAE"].lca_p10   = 0.02     # was 0.03  (lower lifecycle penalty)
    METHODS["Mineral OAE"].lca_p90   = 0.06     # was 0.12
    METHODS["Mineral OAE"].cost_p90  = 120      # was 165   (grinding-dominated opex falls)
    METHODS["Mineral OAE"].note      = "grinding energy halved (OurCo process X)"

then re-run build_v2.py (or the Screener). The breakeven site-efficiency and P(investable)
will move accordingly. Add a brand-new method by copying any Method(...) block and giving it
a new name. Nothing else in the codebase needs to change — every consumer imports from here.

Guardrails when you edit: keep p10 < p90; costs are USD/nominal-tonne at scale; lca_penalty
and efficiency are fractions in [0, 1]; issuance is a probability in [0, 1]. The provided
`validate()` checks these and prints any problem.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Method:
    """All editable assumptions for one carbon-removal method. Edit the numbers freely."""
    # ---- gross cost, USD per nominal (design) tonne, at scale, 10th–90th pct ----
    cost_p10: float
    cost_p90: float
    # ---- lifecycle-emissions penalty (fraction of removal lost to LCA), 10th–90th pct ----
    lca_p10: float
    lca_p90: float
    # ---- how efficiency is determined ----
    eff_kind: str                       # 'atlas_oae' | 'pathway' | 'exempt'
    # ---- realized-removal efficiency, ONLY for eff_kind == 'pathway', 10th–90th pct ----
    eff_p10: Optional[float] = None
    eff_p90: Optional[float] = None
    # ---- near-term probability that credits are actually issued, 10th–90th pct ----
    issuance_p10: float = 0.01
    issuance_p90: float = 0.10
    # ---- is realized removal sensitive to site ocean physics? (reporting flag) ----
    sensitive: bool = True
    # ---- provenance + free-text note (why these numbers; edit when you change them) ----
    source: str = ""
    note: str = ""


# =====================================================================================
# THE ASSUMPTION SHEET. Edit values here. Sources are in paper/REFERENCES.md + Appendix B/B.1.
# =====================================================================================
METHODS = {
    "Mineral OAE": Method(
        cost_p10=30, cost_p90=165,              # olivine, grinding-dominated opex (Renforth&Henderson 2017; Strefler 2018)
        lca_p10=0.03, lca_p90=0.12,             # grain-size-dependent grinding+transport emissions (Foteinis 2023)
        eff_kind="atlas_oae", sensitive=True,   # efficiency read from the Zhou atlas at the deployment site
        issuance_p10=0.05, issuance_p90=0.15,   # OAE has the best near-term issuance odds (still low)
        source="Renforth&Henderson 2017; Strefler 2018; Foteinis 2023",
        note="grinding energy sets both cost and LCA; the main lever for an innovator"),
    "Electrochemical OAE": Method(
        cost_p10=60, cost_p90=200,              # BPED electrodialysis (Eisaman 2012; Ebb/Planetary route envelopes)
        lca_p10=0.04, lca_p90=0.15,             # electricity-driven; grid carbon sets it (Isometric measured 5.27% on Planetary)
        eff_kind="atlas_oae", sensitive=True,
        issuance_p10=0.03, issuance_p90=0.12,
        source="Eisaman 2012; Isometric deduction on Planetary",
        note="LCA is grid-carbon-driven; a clean-power PPA is the lever"),
    "DOC / DIC stripping": Method(
        cost_p10=100, cost_p90=400,             # direct ocean capture / DIC stripping (Eisaman 2018; Equatic disclosures)
        lca_p10=0.08, lca_p90=0.30,             # electrolysis energy; H2 co-product credit swings it widely
        eff_kind="exempt", sensitive=False,     # physics-exempt: removal not gated by air-sea equilibration efficiency
        issuance_p10=0.01, issuance_p90=0.05,
        source="Eisaman 2018; Equatic disclosures",
        note="H2 co-product credit is the biggest LCA lever"),
    "Marine biomass sinking": Method(
        cost_p10=400, cost_p90=3000,            # macroalgae cultivation+harvest+sinking (Coleman 2022; DeAngelo 2023)
        lca_p10=0.15, lca_p90=0.50,             # vessel fuel + cultivation; plus an air-sea re-equilibration loss (in eff, not lca)
        eff_kind="pathway", eff_p10=0.05, eff_p90=0.40,  # realized atmospheric-removal fraction ~25% central (Hurd 2024; Bach 2021)
        sensitive=True, issuance_p10=0.002, issuance_p90=0.02,
        source="Coleman 2022; Bach 2021; Hurd 2024",
        note="binding drag is realized efficiency (~25%), not LCA; raising durable-fraction is the lever"),
    "Terrestrial burial (control)": Method(
        cost_p10=14, cost_p90=120,              # wood-vault / anoxic burial control (Zeng 2022, 2024)
        lca_p10=0.02, lca_p90=0.08,             # harvest + burial logistics; preservation-limited not equilibration-limited
        eff_kind="exempt", sensitive=False,
        issuance_p10=0.05, issuance_p90=0.25,
        source="Zeng 2022, 2024",
        note="physics-exempt control case; highest near-term verified-tonne yield per dollar"),
    "Iron fertilization": Method(
        cost_p10=100, cost_p90=2000,            # dosing cheap; cost is efficiency+MRV driven (Ward 2025)
        lca_p10=0.05, lca_p90=0.15,             # ship time; LCA is NOT the binding drag here
        eff_kind="pathway", eff_p10=0.005, eff_p90=0.05,  # ~2% durably sequestered (Ward 2025; NASEM 2022; Smetacek 2012)
        sensitive=True, issuance_p10=0.001, issuance_p90=0.02,
        source="Ward 2025; Smetacek 2012; NASEM 2022",
        note="~2% durable fraction dominates; nothing an innovator changes on LCA rescues the economics"),
}


# LCA_NOTES: what the lca_penalty means per method, so an editor sets it for the right reason.
# (Energy intensities and dominant drivers are tabulated in paper Appendix B.1.)
LCA_NOTES = {
    "Mineral OAE": "grinding (224-748 kWh/t) + transport; grain size sets it",
    "Electrochemical OAE": "electrodialysis electricity (650-1850 kWh/t); grid carbon sets it",
    "DOC / DIC stripping": "electrolysis energy (380 to >2500 kWh/t); H2 credit swings it",
    "Marine biomass sinking": "vessel fuel + cultivation; re-equilibration loss counted in efficiency",
    "Terrestrial burial (control)": "harvest + burial logistics; low",
    "Iron fertilization": "ship time; low, and not the binding constraint",
}

# Monte-Carlo correlation between cost and LCA (shared latent: energy-intensive -> both higher).
COST_LCA_RHO = 0.5


def validate():
    """Sanity-check every editable field. Prints problems; returns True if all clean."""
    ok = True
    for name, m in METHODS.items():
        for lo, hi, lbl in [(m.cost_p10, m.cost_p90, "cost"), (m.lca_p10, m.lca_p90, "lca"),
                            (m.issuance_p10, m.issuance_p90, "issuance")]:
            if not (lo < hi):
                print(f"[{name}] {lbl}: p10 ({lo}) must be < p90 ({hi})"); ok = False
        if not (0 <= m.lca_p10 <= 1 and 0 <= m.lca_p90 <= 1):
            print(f"[{name}] lca must be a fraction in [0,1]"); ok = False
        if m.eff_kind == "pathway" and (m.eff_p10 is None or m.eff_p90 is None):
            print(f"[{name}] eff_kind 'pathway' needs eff_p10/eff_p90"); ok = False
        if m.eff_kind not in ("atlas_oae", "pathway", "exempt"):
            print(f"[{name}] eff_kind must be atlas_oae|pathway|exempt"); ok = False
    print("priors OK" if ok else "priors have problems (see above)")
    return ok


# ---- Back-compatible views the rest of the codebase consumes (do not edit; edit METHODS above) ----
METHODS_V2 = {
    name: dict(cost=(m.cost_p10, m.cost_p90), lca=(m.lca_p10, m.lca_p90),
               eff_kind=m.eff_kind, sensitive=m.sensitive,
               **({"eff": (m.eff_p10, m.eff_p90)} if m.eff_kind == "pathway" else {}))
    for name, m in METHODS.items()
}
ISSUANCE_NEARTERM = {name: (m.issuance_p10, m.issuance_p90) for name, m in METHODS.items()}


if __name__ == "__main__":
    validate()
    print(f"\n{len(METHODS)} methods loaded. Edit values in METHODS above and re-run build_v2.py.")
