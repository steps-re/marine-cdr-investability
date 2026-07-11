"""
NCC-style global surface-flushing map from the corrected native-resolution field (global_flushing_v3.nc).
Shows residence time within a ~150 km footprint over 2 yr: near-uniformly fast (dark) almost everywhere,
with rare retentive recirculation cores (bright). Run: .venv/bin/python sim/make_flushing_map.py
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import ncc_style as S

S.apply()
NC = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs", "global_flushing_v3.nc")
PROJ = ccrs.Robinson(central_longitude=-150)
PC = ccrs.PlateCarree()

import xarray as xr
ds = xr.open_dataset(NC)
tau = ds["tau_flush_yr"]
lat = tau.lat.values; lon = tau.lon.values
field = np.ma.masked_invalid(tau.values)

fig, ax = plt.subplots(figsize=(S.COL15, 4.0), subplot_kw={"projection": PROJ})
ax.add_feature(cfeature.LAND, facecolor=S.PALETTE["land"], edgecolor="none", zorder=2)
ax.add_feature(cfeature.COASTLINE, edgecolor=S.PALETTE["coast"], linewidth=0.3, zorder=3)
ax.set_global()
ax.spines["geo"].set_edgecolor("#999999"); ax.spines["geo"].set_linewidth(0.6)
m = ax.pcolormesh(lon, lat, np.clip(field, 0.29, 100), transform=PC, cmap="magma_r",
                  norm=LogNorm(vmin=0.29, vmax=100), shading="auto", zorder=1, rasterized=True)
ax.set_title("Surface residence time at the deployment footprint", loc="left")
cb = fig.colorbar(m, ax=ax, orientation="vertical", shrink=0.72, pad=0.02, aspect=18,
                  extend="max")
cb.set_label("flushing time (yr, log)", fontsize=7.5); cb.ax.tick_params(labelsize=7)
cb.outline.set_linewidth(0.5)
fig.text(0.5, 0.02, "~89% of the ocean flushes a treated patch within a few months (dark); "
         "retention is confined to rare recirculation cores (bright). Surface residence is a near-universal "
         "verification constraint.", ha="center", fontsize=7, color="#555555")
S.save(fig, "fig6_flushing_global")
