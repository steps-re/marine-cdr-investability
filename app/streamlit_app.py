"""
Marine CDR Investability Screener — Steps Ventures.
Unified with the peer-review model (v2): realized fraction = efficiency x (1 - LCA), conditional
on issuance, and near-term issuance probability is reported separately as the binding gate.
Method + location -> P(investable if issued), issuance probability, net cost, physics breakeven.
All assumptions are editable in the browser (and in src/priors.py). First-order screen, not a bankable TEA.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st
import priors
import investability_v2 as iv

st.set_page_config(page_title="Marine CDR Investability Screener", layout="wide")
LK = np.load(os.path.join(os.path.dirname(__file__), "fkin_lookup.npz"))
TLAT, TLONG, VALID = LK["tlat"], LK["tlong"], LK["valid"]
FKH = {1: LK["fk1"], 5: LK["fk5"], 10: LK["fk10"]}


def fkin_at(lat, lon, horizon):
    arr = FKH[horizon]
    lon360 = lon % 360
    dlon = (TLONG - lon360 + 180) % 360 - 180
    d = (dlon * np.cos(np.radians(lat))) ** 2 + (TLAT - lat) ** 2
    d = np.where(VALID, d, np.inf)
    j, i = np.unravel_index(np.argmin(d), d.shape)
    return float(arr[j, i]), float(np.sqrt(d[j, i]))


SCENARIOS = ["Literature range (full uncertainty)", "Optimistic", "Average / central", "Pessimistic"]


def band(p10, p90, scenario, higher_better=False):
    """Turn a (10th, 90th) prior into the (low, high) range for the chosen scenario.
    higher_better=False for cost/LCA (low is good); True for efficiency/issuance (high is good).
    """
    g = float(np.sqrt(p10 * p90))                       # lognormal median
    if scenario == "Literature range (full uncertainty)":
        return (p10, p90)
    if scenario == "Average / central":
        return (round(g * 0.9, 4), round(g * 1.1, 4))
    favorable_low = (p10, g)                             # the good half is the LOW half...
    favorable_high = (g, p90)                            # ...or the HIGH half
    if higher_better:
        return favorable_high if scenario == "Optimistic" else favorable_low
    return favorable_low if scenario == "Optimistic" else favorable_high


PRESETS = {
    "Custom location": None,
    "Captura — Kona HI (DOC)": (19.7, -156.0),
    "Ebb Carbon — Salish Sea (elec-OAE)": (48.1, -123.0),
    "Planetary — Halifax NS (elec-OAE)": (44.6, -63.6),
    "Vesta — Duck NC (mineral OAE)": (36.2, -75.75),
    "Equatic — Singapore (DOC)": (1.3, 103.8),
    "Gigablue — S Pacific gyre (iron)": (-35.0, -160.0),
    "Running Tide — off Iceland (kelp)": (63.0, -20.0),
}

st.title("Marine CDR Investability Screener")
st.caption("Does the ocean cash the check? A physics-based due-diligence layer for marine carbon-removal "
           "deals. Steps Ventures. Model: realized = efficiency x (1 - LCA), conditional on issuance; near-term "
           "issuance is the separate binding gate. First-order screen over literature-anchored, editable priors.")

c1, c2 = st.columns([1, 2])
with c1:
    method = st.selectbox("Method archetype", list(priors.METHODS))
    m = priors.METHODS[method]
    atlas = (m.eff_kind == "atlas_oae")
    price = st.slider("Credit price ($/tCO₂)", 50, 600, 350, 10)
    horizon = st.selectbox("Realized-efficiency horizon (yr)", [1, 5, 10], index=1)
    scenario = st.radio("Assumption scenario", SCENARIOS, index=0,
                        help="Presets the cost / LCA / efficiency / issuance defaults. "
                             "'Literature range' keeps the full 10th–90th-percentile uncertainty; "
                             "Optimistic / Average / Pessimistic collapse toward the favorable, central, "
                             "or unfavorable end. You can still fine-tune any value below.")
    if atlas:
        preset = st.selectbox("Location", list(PRESETS))
        if PRESETS[preset]:
            lat, lon = PRESETS[preset]
            st.write(f"lat **{lat}**, lon **{lon}**")
        else:
            lat = st.number_input("Latitude", -79.0, 89.0, 20.0)
            lon = st.number_input("Longitude", -180.0, 180.0, -156.0)
    else:
        kind = "a pathway prior" if m.eff_kind == "pathway" else "physics-exempt (efficiency = 1)"
        st.info(f"{method}: efficiency is {kind}, so a map location does not set it.")
        lat, lon = 20.0, -156.0

    # scenario-derived defaults (the user can still fine-tune each)
    cost_d = band(float(m.cost_p10), float(m.cost_p90), scenario)
    lca_d = band(float(m.lca_p10), float(m.lca_p90), scenario)
    iss_d = band(float(m.issuance_p10), float(m.issuance_p90), scenario, higher_better=True)
    kp = f"{method}|{scenario}"                         # key prefix: reset widgets when method/scenario changes

    st.markdown("---")
    with st.expander(f"✎ Edit assumptions — {scenario.split(' (')[0]} defaults, tune freely"):
        st.caption("These start from the paper's literature priors, collapsed to the scenario you picked, as "
                   "(low, high) ranges. Change any of them to model your own economics or an innovation, and "
                   "everything updates live. Same numbers as src/priors.py; full guide in CUSTOMIZE.md (open repo).")
        e1, e2 = st.columns(2)
        with e1:
            c_lo = st.number_input("Gross cost — low ($/t)", 1.0, 5000.0, float(cost_d[0]), 1.0, key=kp + "clo")
        with e2:
            c_hi = st.number_input("Gross cost — high ($/t)", 1.0, 5000.0, float(cost_d[1]), 1.0, key=kp + "chi")
        lca_lo, lca_hi = st.slider("Lifecycle-emissions penalty λ (fraction of removal lost)",
                                   0.0, 0.9, (float(lca_d[0]), float(lca_d[1])), 0.01, key=kp + "lca")
        st.caption("λ driver: " + priors.LCA_NOTES.get(method, ""))
        clo, chi = min(c_lo, c_hi), max(c_lo, c_hi)
        if chi <= clo:
            chi = clo * 1.05
        overrides = {"cost": (clo, chi), "lca": (lca_lo, lca_hi)}
        if m.eff_kind == "pathway":
            eff_d = band(float(m.eff_p10), float(m.eff_p90), scenario, higher_better=True)
            eff_lo, eff_hi = st.slider("Realized-removal efficiency (fraction of gross)",
                                       0.001, 0.95, (float(eff_d[0]), float(eff_d[1])), 0.005, key=kp + "eff")
            overrides["eff"] = (eff_lo, eff_hi)
        iss_lo, iss_hi = st.slider("Near-term issuance probability (do you get paid yet)",
                                   0.0005, 0.6, (float(iss_d[0]), float(iss_d[1])), 0.005, key=kp + "iss")
        overrides["issuance"] = (iss_lo, iss_hi)

rng = np.random.default_rng(0)
if atlas:
    fk, snap = fkin_at(lat, lon, horizon)
    fk_samp = np.clip(rng.normal(fk, 0.10, 20000), 0.02, 0.95)
else:
    fk, snap, fk_samp = None, 0.0, None
s = iv.sample_priors(method, 20000, rng, overrides=overrides)
nc = iv.net_cost(s, fk_samp)
p_inv_cond = float(np.mean(nc < price))
netcost_med = float(np.median(nc))
p_iss = float(np.median(iv.sample_issuance(method, 20000, rng, overrides=overrides)))
p_paid = p_inv_cond * p_iss
be = iv.breakeven_fkin(method, price, 12000, np.random.default_rng(1), overrides=overrides)[0] if atlas else None

with c1:
    st.metric("P(investable) — conditional on credits being issued", f"{p_inv_cond*100:.0f}%")
    st.metric("Median net cost", f"${netcost_med:,.0f}/tCO₂")
    st.metric("Near-term issuance probability", f"{p_iss*100:.0f}%")
    st.caption(f"Unconditional P(paid today) ≈ **{p_paid*100:.1f}%** (investable × issued). "
               "Verification, not chemistry or cost, is the binding near-term gate.")
    if atlas:
        st.metric("Atlas efficiency f_kin at site", f"{fk:.2f}")
        st.metric(f"Physics breakeven at ${price}", "never clears" if (be is None or np.isnan(be)) else f"f_kin ≥ {be:.2f}")
        if snap > 1.0:
            st.caption(f"⚠ nearest modeled ocean cell is ~{snap:.1f}° away (coastal/enclosed — coarse).")

with c2:
    fig, ax = plt.subplots(figsize=(7.5, 5))
    if atlas:
        grid = np.linspace(0.05, 1.0, 60)
        curve = np.array([iv.net_cost(s, np.full(s["cost"].shape, g)) for g in grid])
        ax.plot(grid, np.median(curve, axis=1), color="tab:blue", lw=2)
        ax.fill_between(grid, np.percentile(curve, 25, axis=1), np.percentile(curve, 75, axis=1),
                        color="tab:blue", alpha=0.15)
        ax.scatter([fk], [netcost_med], color="black", zorder=5, s=80)
        ax.annotate("this site", (fk, netcost_med), xytext=(6, 6), textcoords="offset points")
        ax.set_xlabel(f"Air-sea equilibration efficiency f_kin ({horizon}-yr, Zhou 2024)")
    else:
        ax.axhline(netcost_med, color="tab:green", lw=2, ls="--", label="median net cost")
        ax.set_xlabel("efficiency is a method prior / exempt — not a map location")
        ax.set_xticks([])
    ax.axhspan(50, price, color="green", alpha=0.08)
    ax.axhline(price, color="grey", ls=":", label=f"credit price ${price}")
    ax.set_yscale("log"); ax.set_ylim(30, max(2000, netcost_med * 3))
    ax.set_ylabel("Net cost per creditable tonne ($/tCO₂, log)")
    ax.set_title(f"{method} — net cost (conditional on issuance)")
    ax.legend(fontsize=8); ax.grid(True, which="both", alpha=0.2)
    st.pyplot(fig)

st.caption("Realized fraction = efficiency × (1 − LCA), conditional on issuance; net cost = gross cost / realized. "
           "Issuance probability is reported separately (the near-term gate). Priors are editable above (✎) and in "
           "src/priors.py. Sources: Zhou 2024 atlas; Ward 2025, Hurd 2024, Bach 2025 (biology); Foteinis 2023 (LCA); "
           "Isometric protocols. Open code + CUSTOMIZE.md: github.com/steps-re/marine-cdr-investability.")
