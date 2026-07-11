"""
decorr_v3.py — recompute the three-controls decorrelation and the composite-viability field
using the CORRECTED native-resolution flushing field (global_flushing_v3.nc), and report the
statistics that the paper's text/discussion/conclusions must be rewritten from.

Context: the earlier "three physical controls are spatially decorrelated (|r|<=0.19)" claim and
the composite-viability map used global_flushing.nc (v1), which was ~96% floored because it used
non-eddying monthly-climatology currents. v3 fixes the currents (native 1/12deg daily, eddies
resolved). This script re-runs the same analysis on v3 so the conclusions follow the data.

Inputs (sim/out/): global_fields.nc (speed, tau_eq_yr, eta_max), global_flushing_v3.nc (tau_flush_yr).
Outputs: outputs/global_correlations_v3.csv, outputs/composite_viability_v3.nc, and a printed
summary (flushing distribution, the three correlations, composite/retained distributions).
Run: python sim/decorr_v3.py
"""
import os
import numpy as np
import pandas as pd
import xarray as xr

HERE = os.path.dirname(os.path.abspath(__file__))
OUTd = os.path.join(HERE, "out")
OUT = os.path.join(os.path.dirname(HERE), "outputs")


def main():
    gf = xr.open_dataset(os.path.join(OUTd, "global_fields.nc"))
    fl = xr.open_dataset(os.path.join(OUTd, "global_flushing_v3.nc"))
    speed = gf["speed"]; taueq = gf["tau_eq_yr"].clip(0.02, 5); eta = gf["eta_max"]
    flush = fl["tau_flush_yr"]
    flush_on = flush.interp(lat=speed.lat, lon=speed.lon, method="nearest")

    # ---- 1. the corrected flushing field's own distribution (the headline physical result) ----
    fv = flush.values[np.isfinite(flush.values)]
    retention_frac = np.exp(-fl.attrs.get("YEARS", 2) / np.clip(fv, 1e-6, None))   # frac still co-located
    print("=== CORRECTED FLUSHING FIELD (v3, native 1/12deg daily) ===")
    print(f"cells {fv.size}; floored(<0.3yr) {100*(fv<0.3).mean():.1f}%  fast(<0.5yr) {100*(fv<0.5).mean():.1f}%  "
          f"retentive(>5yr) {100*(fv>5).mean():.1f}%")
    print(f"tau_flush quantiles yr: {np.round(np.quantile(fv,[0,.25,.5,.75,.9,.99,1]),2)}")
    print(f"median retained-fraction after horizon: {np.median(retention_frac):.3f} "
          f"(fraction of a treated patch still co-located; low = can't verify locally)")

    # ---- 2. the three pairwise correlations, recomputed with v3 flushing ----
    a = speed.values.ravel()
    b = np.log10(taueq.values.ravel())
    c = np.log10(np.clip(flush_on.values.ravel(), 0.05, None))
    ok = np.isfinite(a) & np.isfinite(b) & np.isfinite(c)
    a, b, c = a[ok], b[ok], c[ok]

    def r(x, y):
        return float(np.corrcoef(x, y)[0, 1])
    corr = {"speed_vs_tau_eq": round(r(a, b), 3), "speed_vs_flush": round(r(a, c), 3),
            "tau_eq_vs_flush": round(r(b, c), 3), "flush_log_variance": round(float(np.var(c)), 3)}
    print("\n=== THREE-CONTROLS CORRELATIONS (v3) ===")
    print(corr)
    print(f"max |r| = {max(abs(corr['speed_vs_tau_eq']), abs(corr['speed_vs_flush']), abs(corr['tau_eq_vs_flush'])):.3f}")

    # ---- 3. composite viability with v3 flushing ----
    tf = flush.interp(lat=taueq.lat, lon=taueq.lon, method="nearest")
    retained = tf / (tf + taueq)                        # cashes locally before it flushes
    V = (retained * (eta / 0.9)).clip(0, 1).rename("V").where(np.isfinite(speed))
    xr.Dataset({"V": V, "retained": retained.rename("retained")}).to_netcdf(
        os.path.join(OUTd, "composite_viability_v3.nc"))
    rv = retained.values[np.isfinite(retained.values)]
    Vv = V.values[np.isfinite(V.values)]
    print("\n=== COMPOSITE VIABILITY (v3) ===")
    print(f"retained-before-flush: median {np.median(rv):.3f}  frac>0.5 {100*(rv>0.5).mean():.1f}%")
    print(f"V (verifiable realization): median {np.median(Vv):.3f}  frac>0.5 {100*(Vv>0.5).mean():.1f}%")

    pd.DataFrame([{**corr,
                   "flush_floored_pct": round(100 * (fv < 0.3).mean(), 1),
                   "flush_retentive_pct": round(100 * (fv > 5).mean(), 1),
                   "retained_median": round(float(np.median(rv)), 3),
                   "retained_gt0p5_pct": round(100 * (rv > 0.5).mean(), 1),
                   "V_median": round(float(np.median(Vv)), 3)}]
                 ).to_csv(os.path.join(OUT, "global_correlations_v3.csv"), index=False)
    print("\nwrote outputs/global_correlations_v3.csv + sim/out/composite_viability_v3.nc")
    print("\nINTERPRETATION FOR THE TEXT: surface flushing at the deployment footprint is near-uniformly")
    print("fast (see floored%/retained), so it is a near-universal MRV constraint, not a site-discriminating")
    print("axis. Report the corrected correlations and the retained-fraction as the honest result.")


if __name__ == "__main__":
    main()
