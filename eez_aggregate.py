"""
Aggregate the published atlas OAE efficiency (f_kin, 5-yr, season-averaged) by national
Exclusive Economic Zone, and overlay which nations are investing in engineered mCDR.
Produces the national wedge: who invests vs the realized-efficiency potential of their waters.

Outputs: outputs/eez_fkin.csv (ranked) + outputs/fig_eez_map.png (choropleth + investor markers).
"""
import os
os.environ.setdefault("OGR_GEOJSON_MAX_OBJ_SIZE", "0")
import numpy as np
import pandas as pd
import geopandas as gpd
import xarray as xr
from shapely import make_valid
from shapely.geometry import Point
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__); OUT = os.path.join(HERE, "outputs")
os.makedirs(OUT, exist_ok=True)

# --- 1) atlas 5-yr season-averaged f_kin field -> valid cell points ---
ds = xr.open_dataset(os.path.join(HERE, "data", "OAE_efficiency_maps_alltime.nc"))
fk2d = np.nanmean(ds["OAE_efficiency"].values[:, 59, :, :], axis=0)   # (nlat, nlon), 5 yr
tlat = ds["TLAT"].values; tlon = ds["TLONG"].values
mask = np.isfinite(fk2d)
lat = tlat[mask]; lon = ((tlon[mask] + 180) % 360) - 180; val = fk2d[mask]
cells = gpd.GeoDataFrame({"fkin": val}, geometry=[Point(x, y) for x, y in zip(lon, lat)], crs="EPSG:4326")
print("valid atlas cells:", len(cells))

# --- 2) EEZ polygons (raw, per-territory; no dissolve). Make valid + simplify for a fast, robust sjoin. ---
print("loading EEZ polygons (zipped shapefile)...")
eez = gpd.read_file(os.path.join(HERE, "data", "eez.zip"))[["sovereign1", "geometry"]].dropna(subset=["sovereign1"])
eez["geometry"] = eez.geometry.simplify(0.1).apply(lambda g: make_valid(g))
eez = eez[~eez.geometry.is_empty & eez.geometry.notna()]
print("EEZ territory polygons:", len(eez), "| sovereigns:", eez["sovereign1"].nunique())

# --- 3) spatial join cells -> EEZ (raw), aggregate mean f_kin by sovereign ---
joined = gpd.sjoin(cells, eez, how="inner", predicate="within")
agg = (joined.groupby("sovereign1")["fkin"].agg(mean_fkin_5yr="mean", n_cells="count").reset_index())
agg = agg[agg["n_cells"] >= 20].sort_values("mean_fkin_5yr", ascending=False)

# --- 4) national engineered-mCDR investment overlay (from literature/04; coarse, defensible) ---
# 2 = active engineered mCDR public/near-public program; 1 = blue-carbon/assessment; 0 = none noted
INVEST = {
    "United States": 2, "Canada": 2, "United Kingdom": 2, "Norway": 2, "Singapore": 2,
    "Australia": 2, "New Zealand": 1, "Chile": 2, "Iceland": 1, "Japan": 1,
    "South Korea": 1, "China": 1, "Brazil": 1, "India": 1, "Saudi Arabia": 1, "Netherlands": 2,
}
agg["invest_level"] = agg["sovereign1"].map(INVEST).fillna(0).astype(int)
agg.to_csv(os.path.join(OUT, "eez_fkin.csv"), index=False)
print("\n=== EEZ mean f_kin (5yr), investing nations flagged (2=engineered,1=bluecarbon/assess) ===")
print(agg[agg["invest_level"] > 0].to_string(index=False))
print("\nTop-12 highest-efficiency EEZs (any nation, n>=20 cells):")
print(agg.head(12)[["sovereign1", "mean_fkin_5yr", "n_cells", "invest_level"]].to_string(index=False))
print("\nBottom-8 (worst physics):")
print(agg.tail(8)[["sovereign1", "mean_fkin_5yr", "n_cells", "invest_level"]].to_string(index=False))

# --- 5a) Figure 4a: choropleth of EEZ mean f_kin + investor markers (from joined cell coords) ---
eez_plot = eez.merge(agg, on="sovereign1", how="left")
# marker + label position = mean coordinate of the atlas cells actually in each sovereign's EEZ
cell_pos = joined.groupby("sovereign1").apply(
    lambda g: (float(g.geometry.x.mean()), float(g.geometry.y.mean())), include_groups=False)
fig, ax = plt.subplots(figsize=(15, 7.5))
eez_plot.plot(column="mean_fkin_5yr", cmap="RdYlGn", vmin=0.2, vmax=0.85, legend=True,
              legend_kwds={"label": "EEZ mean OAE realized efficiency f_kin (5-yr, Zhou 2024)", "shrink": 0.5},
              missing_kwds={"color": "whitesmoke"}, ax=ax, edgecolor="grey", linewidth=0.1)
inv_sov = [s for s, lv in INVEST.items() if lv == 2 and s in cell_pos.index]
for s in inv_sov:
    x, y = cell_pos[s]
    ax.scatter([x], [y], marker="o", s=55, facecolor="none", edgecolor="black", linewidth=1.6, zorder=6)
    ax.annotate(s, (x, y), fontsize=7, fontweight="bold", xytext=(4, 4), textcoords="offset points", zorder=7)
ax.scatter([], [], marker="o", s=55, facecolor="none", edgecolor="black", label="investing in engineered mCDR")
ax.set_xlim(-180, 180); ax.set_ylim(-85, 90); ax.set_aspect("equal")
ax.set_title("Who invests in engineered marine CDR vs the realized-efficiency potential of their waters\n"
             "(circles = nations with engineered-mCDR public programs; color = OAE f_kin, red = slow/poor)")
ax.set_xlabel("longitude"); ax.set_ylabel("latitude"); ax.legend(loc="lower left", fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_eez_map.png"), dpi=150)
print("\nsaved -> outputs/fig_eez_map.png")

# --- 5b) Figure 4b: ranked bar (cleaner, robust to map issues) of investing + notable nations ---
notable = agg[(agg["invest_level"] > 0) | (agg["n_cells"] >= 60)].copy().sort_values("mean_fkin_5yr")
cmap = {0: "#bdbdbd", 1: "#fdae61", 2: "#2c7fb8"}
fig2, ax2 = plt.subplots(figsize=(9, 11))
ax2.barh(notable["sovereign1"], notable["mean_fkin_5yr"],
         color=[cmap[v] for v in notable["invest_level"]])
ax2.set_xlabel("EEZ mean OAE realized efficiency f_kin (5-yr, Zhou 2024)")
ax2.set_title("National EEZ air-sea efficiency vs mCDR investment\n"
              "blue = engineered-mCDR program, orange = blue-carbon/assessment, grey = none")
ax2.axvline(0.52, color="red", ls=":", lw=1)
ax2.text(0.525, 0.5, "elec-OAE breakeven ~0.52 @ \\$350", fontsize=7, color="red", rotation=90, va="bottom")
ax2.margins(y=0.01); fig2.tight_layout(); fig2.savefig(os.path.join(OUT, "fig_eez_bars.png"), dpi=150)
print("saved -> outputs/fig_eez_bars.png")
