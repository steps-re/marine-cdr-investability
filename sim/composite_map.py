"""
The unifying figure: a global map of VERIFIABLE REALIZATION POTENTIAL for surface ocean CDR, fusing
the three decorrelated controls into one physical index:
    V = [ tau_flush / (tau_flush + tau_eq) ] * eta_max
- tau_flush/(tau_flush+tau_eq) = fraction of an anomaly that equilibrates locally BEFORE it flushes
  out of the neighbourhood (retained long enough to cash AND be verified in place).
- eta_max = carbonate capacity ceiling (mol CO2 per mol alkalinity).
Where V is high the ocean cashes the check where you can see it; where V is low the removal (if any)
happens downstream, unattributable. Real company deployments are overlaid.
Output: outputs/fig_composite_viability.png + outputs/composite_site_values.csv
"""
import os, sys
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
from fetch_hycom import SITES
OUTd = os.path.join(HERE, "out")
OUT = os.path.join(os.path.dirname(HERE), "outputs"); os.makedirs(OUT, exist_ok=True)

# real engineered-mCDR deployment coordinates (lat, lon, label)
DEPLOY = [(44.68, -63.60, "Planetary"), (41.29, -72.90, "CREW"), (58.0, 6.9, "CarbonRun*"),
          (48.1, -123.0, "Ebb"), (1.29, 103.8, "Equatic"), (19.7, -156.0, "Captura"),
          (36.18, -75.75, "Vesta"), (-45.5, 179.0, "Gigablue"), (64.3, -22.1, "RunningTide"),
          (54.0, 4.0, "SeaO2"), (44.0, 35.0, "Rewind")]


def main():
    gf = xr.open_dataset(os.path.join(OUTd, "global_fields.nc"))
    fl = xr.open_dataset(os.path.join(OUTd, "global_flushing_v3.nc"))
    taueq = gf["tau_eq_yr"]; eta = gf["eta_max"]
    tf = fl["tau_flush_yr"].interp(lat=taueq.lat, lon=taueq.lon, method="nearest")
    retained = tf / (tf + taueq)                       # 0..1: cashes before it flushes
    eta_n = eta / 0.9                                   # normalize ceiling (~0.8-0.9)
    V = (retained * eta_n).clip(0, 1).rename("V")
    V = V.where(np.isfinite(gf["speed"]))
    xr.Dataset({"V": V, "retained": retained}).to_netcdf(os.path.join(OUTd, "composite_viability.nc"))

    # sample V at each deployment -- nearest VALID (ocean) cell within a search window, since coastal
    # deployments often fall on a land/NaN cell of the coarse global grid.
    def nearest_valid(da, lat, lon, win=2.0):
        sub = da.sel(lat=slice(lat - win, lat + win), lon=slice(lon - win, lon + win))
        if sub.size == 0 or not np.isfinite(sub).any():
            return np.nan
        la, lo = np.meshgrid(sub.lat.values, sub.lon.values, indexing="ij")
        d = (la - lat) ** 2 + (lo - lon) ** 2
        d = np.where(np.isfinite(sub.values), d, np.inf)
        j, i = np.unravel_index(np.argmin(d), d.shape)
        return float(sub.values[j, i])

    rows = []
    for lat, lon, name in DEPLOY:
        val = nearest_valid(V, lat, lon); rf = nearest_valid(retained, lat, lon)
        rows.append({"deployment": name, "lat": lat, "lon": lon,
                     "verifiable_realization_V": round(val, 3), "retained_frac": round(rf, 3)})
    df = pd.DataFrame(rows).sort_values("verifiable_realization_V", ascending=False)
    df.to_csv(os.path.join(OUT, "composite_site_values.csv"), index=False)
    gmed = float(np.nanmedian(V.values))
    df["below_global_median"] = df["verifiable_realization_V"] < gmed
    print(df.to_string(index=False))
    print(f"\nglobal median V = {gmed:.3f}; deployments below median: "
          f"{int(df['below_global_median'].sum())}/{len(df)}", flush=True)

    fig, ax = plt.subplots(figsize=(13, 7))
    pm = ax.pcolormesh(V.lon, V.lat, V.values, cmap="RdYlGn", vmin=0, vmax=1, shading="auto")
    fig.colorbar(pm, ax=ax, shrink=0.8, label="verifiable realization potential V")
    ax.set_facecolor("#d9d9d9")
    for lat, lon, name in DEPLOY:
        ax.plot(lon, lat, "k^", ms=7, mec="white", mew=0.7)
        ax.annotate(name, (lon, lat), fontsize=7, xytext=(4, 3), textcoords="offset points", color="k")
    ax.set_title("Global verifiable-realization potential for surface ocean CDR\n"
                 "V = retained-before-flush x carbonate capacity. Triangles = real deployments; "
                 "many sit in low-V (fast-flushing / slow-equilibrating) water", fontsize=11)
    ax.set_xlabel("lon"); ax.set_ylabel("lat")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_composite_viability.png"), dpi=140)
    print("saved outputs/fig_composite_viability.png + composite_site_values.csv", flush=True)


if __name__ == "__main__":
    main()
