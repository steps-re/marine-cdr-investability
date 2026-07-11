"""
Three-panel global map: surface current speed | air-sea equilibration time tau_eq | Lagrangian
flushing time tau_flush. Plus a correlation panel showing the three fields are largely DECORRELATED
in space -- fast current is not fast flushing, and neither predicts the equilibration time. That
spatial independence is the point: a site can be fast-flowing yet retentive (recirculating), or slow
yet flushing (through-flow), and equilibration is a separate chemistry/MLD control.
Output: outputs/fig_three_panel.png + outputs/global_correlations.csv
"""
import os
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors

HERE = os.path.dirname(__file__)
OUTd = os.path.join(HERE, "out")
OUT = os.path.join(os.path.dirname(HERE), "outputs"); os.makedirs(OUT, exist_ok=True)

gf = xr.open_dataset(os.path.join(OUTd, "global_fields.nc"))
fl = xr.open_dataset(os.path.join(OUTd, "global_flushing_v3.nc"))
speed = gf["speed"]; taueq = gf["tau_eq_yr"].clip(0.02, 5)
flush = fl["tau_flush_yr"]
flush_on = flush.interp(lat=speed.lat, lon=speed.lon, method="nearest")   # to common grid

fig = plt.figure(figsize=(15, 9))
panels = [(speed, "Surface current speed (m/s)", "viridis", dict(vmin=0, vmax=0.6)),
          (taueq, "Air-sea equilibration time tau_eq (yr)", "plasma", dict(vmin=0.05, vmax=2)),
          (flush.clip(0.1, 100), "Lagrangian flushing time (yr, log)", "cividis",
           dict(norm=matplotlib.colors.LogNorm(vmin=0.2, vmax=100)))]
for idx, (da, title, cmap, kw) in enumerate(panels, 1):
    ax = fig.add_subplot(2, 2, idx)
    pm = ax.pcolormesh(da.lon, da.lat, da.values, cmap=cmap, shading="auto", **kw)
    fig.colorbar(pm, ax=ax, shrink=0.8)
    ax.set_title(title, fontsize=11); ax.set_xlabel("lon"); ax.set_ylabel("lat")
    ax.set_facecolor("#e8e8e8")

# correlation panel: scatter of the three on common ocean cells (log for the times)
a = speed.values.ravel(); b = np.log10(taueq.values.ravel()); c = np.log10(np.clip(flush_on.values.ravel(), 0.05, None))
m = np.isfinite(a) & np.isfinite(b) & np.isfinite(c)
a, b, c = a[m], b[m], c[m]
def r(x, y): return float(np.corrcoef(x, y)[0, 1])
corr = {"speed_vs_tau_eq": round(r(a, b), 3), "speed_vs_flush": round(r(a, c), 3),
        "tau_eq_vs_flush": round(r(b, c), 3)}
pd.DataFrame([corr]).to_csv(os.path.join(OUT, "global_correlations.csv"), index=False)

ax = fig.add_subplot(2, 2, 4)
ax.scatter(a, c, s=2, alpha=0.15, c="#2c7fb8")
ax.set_xlabel("surface current speed (m/s)"); ax.set_ylabel("log10 flushing time (yr)")
ax.set_title(f"Speed vs flushing: r={corr['speed_vs_flush']}\n"
             f"(speed–tau_eq r={corr['speed_vs_tau_eq']}, tau_eq–flush r={corr['tau_eq_vs_flush']})", fontsize=10)
fig.suptitle("Surface speed, equilibration time, and flushing time are spatially DECORRELATED\n"
             "each controls a different part of CDR viability; none substitutes for another", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(os.path.join(OUT, "fig_three_panel.png"), dpi=140)
print("correlations:", corr, flush=True)
print("saved outputs/fig_three_panel.png + global_correlations.csv", flush=True)
