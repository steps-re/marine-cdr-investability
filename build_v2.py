"""
Corrected build (v2) with all reviewer fixes:
- no double-counted chemistry ceiling (atlas f_kin is the sole OAE location efficiency)
- pathway-specific efficiency for biological/iron (not the OAE atlas)
- uncertainty bands (Monte-Carlo priors + atlas season spread)
- multi-horizon (1/5/10/15 yr)
- correlated cost<->LCA priors; binary MRV issuance probability
Outputs: outputs/*_v2.csv and fig_*_v2.png
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from investability_v2 import (METHODS_V2, ISSUANCE_NEARTERM, sample_priors, sample_issuance,
                              net_cost, breakeven_fkin)

HERE = os.path.dirname(__file__); OUT = os.path.join(HERE, "outputs")
LK = np.load(os.path.join(HERE, "app", "fkin_lookup.npz"))
tlat, valid = LK["tlat"], LK["valid"]
FKH = {1: LK["fk1"], 5: LK["fk5"], 10: LK["fk10"], 15: LK["fk15"]}
FK5_SEASONS = LK["fk5_seasons"]           # (season, nlat, nlon)
warea = np.cos(np.radians(tlat))
PRICES = [100, 150, 200, 250, 300, 350, 400, 500]
RNG = np.random.default_rng(20)
OAE = [m for m in METHODS_V2 if METHODS_V2[m]["eff_kind"] == "atlas_oae"]
PATH = [m for m in METHODS_V2 if METHODS_V2[m]["eff_kind"] == "pathway"]


def area_at_fkin_threshold(be, horizon=5):
    fk = FKH[horizon]
    if not np.isfinite(be):
        return 0.0
    m = valid & (fk >= be)
    return float(np.sum(warea[m]) / np.sum(warea[valid]))


# ---- 1) Global investable-area for OAE, with uncertainty bands, multi-horizon ----
rows = []
for method in OAE:
    for H in (1, 5, 10, 15):
        for P in PRICES:
            s = sample_priors(method, 4000, RNG)
            req = s["cost"] / (P * (1 - s["lca"]))   # required atlas f_kin per draw (conditional on issuance)
            areas = np.array([area_at_fkin_threshold(min(r, 1.01), H) if r <= 1 else 0.0
                              for r in req[::20]]) * 100            # subsample draws for speed
            rows.append({"method": method, "horizon_yr": H, "price": P,
                         "area_pct_median": round(float(np.median(areas)), 1),
                         "area_pct_p10": round(float(np.percentile(areas, 10)), 1),
                         "area_pct_p90": round(float(np.percentile(areas, 90)), 1)})
area_df = pd.DataFrame(rows)
area_df.to_csv(f"{OUT}/global_investable_area_v2.csv", index=False)
print("=== corrected investable area (OAE, 5-yr) with bands ===")
print(area_df[area_df.horizon_yr == 5].to_string(index=False))

# ---- 2) Breakeven table (all methods) ----
brows = []
for method in METHODS_V2:
    s = sample_priors(method, 6000, RNG)
    iss = ISSUANCE_NEARTERM[method]
    row = {"method": method, "eff_kind": METHODS_V2[method]["eff_kind"],
           "cost_median": round(float(np.median(s["cost"])), 0),
           "issuance_nearterm": f"{int(iss[0]*100)}-{int(iss[1]*100)}%"}
    for P in (200, 350):
        if METHODS_V2[method]["eff_kind"] == "atlas_oae":
            be, lo, hi = breakeven_fkin(method, P, 6000, RNG)
            row[f"breakeven_fkin@{P}"] = "n/a (>1)" if np.isnan(be) else f"{be:.2f} [{lo:.2f}-{hi:.2f}]"
        else:
            fk = None
            pinv = float(np.mean(net_cost(sample_priors(method, 6000, RNG), fk) < P))
            row[f"breakeven_fkin@{P}"] = f"exempt/pathway; P(inv)={pinv:.2f}"
    brows.append(row)
bt = pd.DataFrame(brows)
bt.to_csv(f"{OUT}/breakeven_table_v2.csv", index=False)
print("\n=== corrected breakevens ===")
print(bt.to_string(index=False))

# ---- 3) Company overlay (corrected: OAE uses atlas f_kin w/ season spread; others pathway) ----
COMP = [
    ("Ebb Carbon", "Electrochemical OAE", 48.1, -123.0), ("Planetary", "Electrochemical OAE", 44.6, -63.6),
    ("Vesta", "Mineral OAE", 36.2, -75.75), ("Captura", "DOC / DIC stripping", 19.7, -156.0),
    ("Equatic", "DOC / DIC stripping", 1.3, 103.8), ("SeaO2", "DOC / DIC stripping", 52.0, 4.3),
    ("Gigablue", "Iron fertilization", -35.0, -160.0), ("Running Tide", "Marine biomass sinking", 63.0, -20.0),
    ("Carboniferous", "Terrestrial burial (control)", 27.0, -91.0),
]
tl, tlon = LK["tlat"], LK["tlong"]


def fkin_samples_at(lat, lon, n=4000):
    lon360 = lon % 360
    dlon = (tlon - lon360 + 180) % 360 - 180
    d = (dlon * np.cos(np.radians(lat)))**2 + (tl - lat)**2
    d = np.where(valid, d, np.inf)
    j, i = np.unravel_index(np.argmin(d), d.shape)
    seas = FK5_SEASONS[:, j, i]                       # 4 seasonal values
    seas = seas[np.isfinite(seas)]
    base = float(np.mean(seas)) if seas.size else float(FKH[5][j, i])
    sd = float(max(np.std(seas), 0.0)) if seas.size else 0.08
    sd = float(np.hypot(sd, 0.10))                    # + ~10% model uncertainty
    return np.clip(RNG.normal(base, sd, n), 0.02, 0.90), base


crows = []
for name, method, lat, lon in COMP:
    kind = METHODS_V2[method]["eff_kind"]
    if kind == "atlas_oae":
        fk, base = fkin_samples_at(lat, lon)
    else:
        fk, base = None, (1.0 if kind == "exempt" else None)
    p200 = float(np.mean(net_cost(sample_priors(method, 8000, RNG),
                 (RNG.choice(fk, 8000) if fk is not None else None)) < 200))
    p350 = float(np.mean(net_cost(sample_priors(method, 8000, RNG),
                 (RNG.choice(fk, 8000) if fk is not None else None)) < 350))
    iss = ISSUANCE_NEARTERM[method]
    iss_mid = (iss[0] + iss[1]) / 2
    crows.append({"company": name, "method": method,
                  "atlas_fkin_5yr": ("n/a" if base is None else round(base, 2)),
                  "P(clears@200|MRV)": round(p200, 2), "P(clears@350|MRV)": round(p350, 2),
                  "issuance_nearterm": f"{int(iss[0]*100)}-{int(iss[1]*100)}%",
                  "P(paid@350) uncond": round(p350 * iss_mid, 3)})
ct = pd.DataFrame(crows)
ct.to_csv(f"{OUT}/company_overlay_v2.csv", index=False)
print("\n=== corrected company overlay ===")
print(ct.to_string(index=False))

# ---- 4) Figure: corrected investable-area vs price, 5-yr, with uncertainty band ----
fig, ax = plt.subplots(figsize=(9, 6))
colors = {"Mineral OAE": "tab:blue", "Electrochemical OAE": "tab:green"}
for method in OAE:
    sub = area_df[(area_df.method == method) & (area_df.horizon_yr == 5)].sort_values("price")
    ax.plot(sub.price, sub.area_pct_median, "-o", color=colors[method], lw=2, label=f"{method} (5-yr)")
    ax.fill_between(sub.price, sub.area_pct_p10, sub.area_pct_p90, color=colors[method], alpha=0.15)
# pathway methods: flat ~0 line annotation
ax.plot(PRICES, [0]*len(PRICES), "-", color="grey", lw=1)
ax.text(110, 3, "marine biomass sinking & iron fertilization: 0% at all prices (pathway efficiency + cost)",
        fontsize=8, color="dimgray")
ax.set_xlabel("Credit price ($/tCO2)"); ax.set_ylabel("% of open ocean investable (median, 10-90 band)")
ax.set_title("How much of the ocean can cash the check - CONDITIONAL ON MRV SUCCEEDING\n"
             "(atlas f_kin = sole OAE efficiency, no double-counted ceiling; bands = correlated cost/LCA priors)")
ax.set_ylim(-2, 102); ax.grid(alpha=0.25); ax.legend(loc="lower right", fontsize=9)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_investable_area_v2.png", dpi=150)
print("\nsaved -> outputs/fig_investable_area_v2.png")

# ---- 5) Issuance-risk figure: the dominant near-term gate ----
fig2, ax2 = plt.subplots(figsize=(9, 5.5))
order = ["Terrestrial burial (control)", "Mineral OAE", "Electrochemical OAE", "DOC / DIC stripping",
         "Marine biomass sinking", "Iron fertilization"]
los = [ISSUANCE_NEARTERM[m][0]*100 for m in order]
his = [ISSUANCE_NEARTERM[m][1]*100 for m in order]
mids = [(l+h)/2 for l, h in zip(los, his)]
y = np.arange(len(order))
ax2.barh(y, his, color="#c7d9ec", edgecolor="#5a7", label="near-term issuance probability range")
ax2.barh(y, los, color="#5a86b3")
for i, m in enumerate(order):
    ax2.text(his[i]+0.5, i, f"{int(los[i])}-{int(his[i])}%", va="center", fontsize=9)
ax2.set_yticks(y); ax2.set_yticklabels(order, fontsize=9); ax2.invert_yaxis()
ax2.set_xlabel("Near-term probability a project actually gets credits ISSUED (%)")
ax2.set_title("The dominant near-term gate is verification, not physics or cost\n"
              "Only Planetary has ever issued mCDR credits; ~0.3% of contracted volume issued (2025-26)")
ax2.set_xlim(0, 30); ax2.grid(axis="x", alpha=0.25)
fig2.tight_layout(); fig2.savefig(f"{OUT}/fig_issuance_risk_v2.png", dpi=150)
print("saved -> outputs/fig_issuance_risk_v2.png")

# ---- 6) Corrected overlay: net cost vs atlas f_kin (conditional on MRV), companies plotted ----
fig3, ax3 = plt.subplots(figsize=(10, 6.3))
fkg = np.linspace(0.05, 1.0, 60)
oae_c = {"Mineral OAE": "tab:blue", "Electrochemical OAE": "tab:green"}
for method in OAE:
    s = sample_priors(method, 8000, RNG)
    nc = np.array([net_cost(s, fk) for fk in fkg])            # (grid, n) conditional on MRV
    ax3.plot(fkg, np.median(nc, axis=1), color=oae_c[method], lw=2, label=method)
    ax3.fill_between(fkg, np.percentile(nc, 25, axis=1), np.percentile(nc, 75, axis=1),
                     color=oae_c[method], alpha=0.15)
for method, col in [("DOC / DIC stripping", "tab:purple"), ("Terrestrial burial (control)", "tab:olive"),
                    ("Marine biomass sinking", "tab:pink"), ("Iron fertilization", "tab:cyan")]:
    s = sample_priors(method, 8000, RNG)
    ax3.axhline(float(np.median(net_cost(s, None))), color=col, lw=2, ls="--",
                label=f"{method}" + (" (exempt)" if METHODS_V2[method]["eff_kind"] == "exempt" else ""))
ax3.axhspan(100, 500, color="grey", alpha=0.12)
for name, method, lat, lon in COMP:
    if METHODS_V2[method]["eff_kind"] != "atlas_oae":
        continue
    fk, base = fkin_samples_at(lat, lon)
    s = sample_priors(method, 4000, RNG)
    y = float(np.median(net_cost(s, base)))
    ax3.scatter([base], [y], color=oae_c[method], edgecolor="black", s=70, zorder=6)
    ax3.annotate(name, (base, y), textcoords="offset points", xytext=(5, 4), fontsize=8)
ax3.set_yscale("log"); ax3.set_ylim(30, 60000)
ax3.set_xlabel("Atlas air-sea equilibration efficiency f_kin (5-yr, Zhou 2024)")
ax3.set_ylabel("Net cost per creditable tonne ($/tCO2, log) - conditional on verification")
ax3.set_title("Corrected overlay: net cost vs air-sea physics (no double-counted ceiling)\n"
              "markers = OAE deployments at atlas f_kin; band = interquartile over cost/LCA priors")
ax3.legend(fontsize=7, loc="upper right"); ax3.grid(True, which="both", alpha=0.2)
fig3.tight_layout(); fig3.savefig(f"{OUT}/fig_overlay_atlas_v2.png", dpi=150)
print("saved -> outputs/fig_overlay_atlas_v2.png")
