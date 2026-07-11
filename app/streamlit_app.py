"""
Marine CDR Investability Screener — Steps Ventures.
Punch in a method + location; get P(investable), the physics breakeven, and the
net-cost-vs-efficiency curve, using the published Zhou 2024 air-sea efficiency atlas
and literature-anchored techno-economic priors. First-order screen, not a bankable TEA.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st
from investability import METHODS, sample_method, net_cost, physics_breakeven

st.set_page_config(page_title="Marine CDR Investability Screener", layout="wide")
LK = np.load(os.path.join(os.path.dirname(__file__), "fkin_lookup.npz"))
TLAT, TLONG, VALID = LK["tlat"], LK["tlong"], LK["valid"]
FKH = {1: LK["fk1"], 5: LK["fk5"], 10: LK["fk10"]}


def fkin_at(lat, lon, horizon):
    arr = FKH[horizon]
    lon360 = lon % 360
    dlon = (TLONG - lon360 + 180) % 360 - 180
    d = (dlon * np.cos(np.radians(lat)))**2 + (TLAT - lat)**2
    d = np.where(VALID, d, np.inf)
    j, i = np.unravel_index(np.argmin(d), d.shape)
    return float(arr[j, i]), float(np.sqrt(d[j, i]))


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
st.caption("Does the ocean cash the check? A physics-based due-diligence layer for marine carbon-removal deals. "
           "Steps Ventures. First-order screen over literature-anchored priors — not a bankable TEA.")

c1, c2 = st.columns([1, 2])
with c1:
    method = st.selectbox("Method archetype", list(METHODS))
    price = st.slider("Credit price ($/tCO₂)", 50, 600, 350, 10)
    horizon = st.selectbox("Realized-efficiency horizon (yr)", [1, 5, 10], index=1)
    preset = st.selectbox("Location", list(PRESETS))
    if PRESETS[preset]:
        lat, lon = PRESETS[preset]
        st.write(f"lat **{lat}**, lon **{lon}**")
    else:
        lat = st.number_input("Latitude", -79.0, 89.0, 20.0)
        lon = st.number_input("Longitude", -180.0, 180.0, -156.0)

    st.markdown("---")
    with st.expander("✎ Edit this method's assumptions — bring your own numbers"):
        st.caption("These are the paper's literature priors, as (low, high) = 10th/90th-percentile "
                   "ranges. Change any of them to model your own costs or an innovation (say a process "
                   "that halves energy, so lower cost and lower lifecycle penalty). Everything updates live. "
                   "Full documentation: the CUSTOMIZE.md guide and src/priors.py in the open repo.")
        _m = METHODS[method]
        e1, e2 = st.columns(2)
        with e1:
            c_lo = st.number_input("Gross cost — low ($/t)", 1.0, 5000.0, float(_m["cost"][0]), 1.0)
        with e2:
            c_hi = st.number_input("Gross cost — high ($/t)", 1.0, 5000.0, float(_m["cost"][1]), 1.0)
        lca_lo, lca_hi = st.slider("Lifecycle-emissions penalty λ (fraction of removal lost)",
                                   0.0, 0.9, (float(_m["lca"][0]), float(_m["lca"][1])), 0.01)
        mrv_lo, mrv_hi = st.slider("MRV survival ν (fraction that survives verification)",
                                   0.02, 0.99, (float(_m["mrv"][0]), float(_m["mrv"][1])), 0.01)
        yv = st.slider("Chemistry / biology yield ceiling", 0.05, 1.0, float(_m["yield_chem"]), 0.05)
        clo, chi = min(c_lo, c_hi), max(c_lo, c_hi)
        if chi <= clo:
            chi = clo * 1.05
        overrides = {"cost": (clo, chi), "lca": (lca_lo, lca_hi), "mrv": (mrv_lo, mrv_hi), "yield_chem": yv}
        defaults = {"cost": tuple(map(float, _m["cost"])), "lca": tuple(map(float, _m["lca"])),
                    "mrv": tuple(map(float, _m["mrv"])), "yield_chem": float(_m["yield_chem"])}
        if overrides != defaults:
            st.info("Showing results for YOUR edited assumptions (defaults changed).")

sensitive = METHODS[method]["sensitive"]
fk, snap = fkin_at(lat, lon, horizon)
rng = np.random.default_rng(0)
s = sample_method(method, 20000, rng, overrides=overrides)
if sensitive:
    fk_samp = np.clip(rng.normal(fk, 0.10, 20000), 0.02, 0.90)
    fk_show = fk
else:
    fk_samp = np.ones(20000)
    fk_show = 1.0
nc = net_cost(s, fk_samp)
p_inv = float(np.mean(nc < price))
netcost_med = float(np.median(nc))
be, _, _ = physics_breakeven(method, price, n=12000, rng=rng, overrides=overrides)

with c1:
    st.metric("P(investable)", f"{p_inv*100:.0f}%")
    st.metric("Median net cost", f"${netcost_med:,.0f}/tCO₂")
    if sensitive:
        st.metric("Atlas efficiency f_kin at site", f"{fk:.2f}")
        st.metric(f"Physics breakeven at ${price}", "never clears" if np.isnan(be) else f"f_kin ≥ {be:.2f}")
        if snap > 1.0:
            st.caption(f"⚠ nearest modeled ocean cell is ~{snap:.1f}° away (coastal/enclosed site — coarse).")
    else:
        st.success("Physics-exempt: removes/stores carbon directly — location air-sea efficiency does not gate it.")

with c2:
    fig, ax = plt.subplots(figsize=(7.5, 5))
    grid = np.linspace(0.05, 1.0, 60)
    if sensitive:
        m = np.array([net_cost(s, g) for g in grid])
        ax.plot(grid, np.median(m, axis=1), color="tab:blue", lw=2)
        ax.fill_between(grid, np.percentile(m, 25, axis=1), np.percentile(m, 75, axis=1), color="tab:blue", alpha=0.15)
        ax.scatter([fk], [netcost_med], color="black", zorder=5, s=80)
        ax.annotate("this site", (fk, netcost_med), xytext=(6, 6), textcoords="offset points")
        ax.set_xlabel(f"Air-sea equilibration efficiency f_kin ({horizon}-yr, Zhou 2024)")
    else:
        ax.axhline(netcost_med, color="tab:green", lw=2, ls="--")
        ax.set_xlabel("f_kin (not applicable — physics-exempt)")
    ax.axhspan(50, price, color="green", alpha=0.08)
    ax.axhline(price, color="grey", ls=":", label=f"credit price ${price}")
    ax.set_yscale("log"); ax.set_ylim(30, max(2000, netcost_med * 3))
    ax.set_ylabel("Net cost per creditable tonne ($/tCO₂, log)")
    ax.set_title(f"{method} — net cost vs air-sea physics")
    ax.legend(fontsize=8); ax.grid(True, which="both", alpha=0.2)
    st.pyplot(fig)

st.caption("Net cost = gross cost / [f_kin × yield × (1−LCA) × MRV]. Priors are editable above (✎) — "
           "bring your own numbers. Sources: NASEM 2022, Renforth & Henderson 2017, He & Tyka 2023, "
           "Ward et al. 2025, Foteinis 2023, Isometric protocols. Efficiency: Zhou et al. 2024 / [C]Worthy atlas. "
           "Open code + CUSTOMIZE.md: github.com/steps-re/marine-cdr-investability.")
