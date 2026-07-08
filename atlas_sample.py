"""
Sample the published Zhou et al. 2024 / [C]Worthy OAE efficiency atlas at exact
deployment coordinates. Efficiency = cumulative atmospheric CO2 uptake / alkalinity
added (the realized air-sea equilibration fraction f_kin), on the CESM POP curvilinear
grid, per injection season (4) and month (0-179 = 15 yr).

Produces atlas f_kin at 1/5/10 yr for (a) He & Tyka validation sites and (b) company
deployments -> outputs/atlas_fkin.csv, to replace the provisional emulator estimates.
"""
import os
import numpy as np
import pandas as pd
import xarray as xr

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "outputs"); os.makedirs(OUT, exist_ok=True)
ds = xr.open_dataset(os.path.join(HERE, "data", "OAE_efficiency_maps_alltime.nc"))
EFF = ds["OAE_efficiency"].values           # (season, N_month, nlat, nlon)
TLAT = ds["TLAT"].values                    # (nlat, nlon)
TLONG = ds["TLONG"].values                  # (nlat, nlon), 0-360
print("efficiency value range:", float(np.nanmin(EFF)), "to", float(np.nanmax(EFF)))
print("seasons:", [str(s) for s in ds["season"].values])


# Valid = cells with modeled efficiency (ocean cells inside a release polygon), any season, mid-run.
VALID = np.isfinite(EFF[:, 60, :, :]).any(axis=0)
print("valid ocean cells in atlas:", int(VALID.sum()), "of", VALID.size)


def nearest_cell(lat, lon):
    """Nearest atlas cell that HAS modeled efficiency (snaps coastal points to nearest ocean cell)."""
    lon360 = lon % 360
    dlon = (TLONG - lon360 + 180) % 360 - 180
    d = (dlon * np.cos(np.radians(lat)))**2 + (TLAT - lat)**2
    d = np.where(VALID, d, np.inf)
    j, i = np.unravel_index(np.argmin(d), d.shape)
    # distance in degrees (approx) to flag far snaps
    snap_deg = float(np.sqrt(d[j, i]))
    return (j, i), snap_deg


def atlas_fkin(lat, lon, horizon_yr):
    """Season-averaged atlas efficiency at nearest valid cell and horizon. Returns (mean, min, max, snap_deg)."""
    (j, i), snap = nearest_cell(lat, lon)
    m = int(np.clip(round(horizon_yr * 12) - 1, 0, EFF.shape[1] - 1))
    vals = EFF[:, m, j, i]                   # 4 seasons
    return float(np.nanmean(vals)), float(np.nanmin(vals)), float(np.nanmax(vals)), snap


# (label, lat, lon, He&Tyka regime / note)
VALIDATION = [
    ("Peru upwelling",    -15.0, -77.0, "fast ~0.8"),
    ("Tasmania",          -43.0, 147.0, "fast"),
    ("Patagonia",         -50.0, -70.0, "fast"),
    ("Brazil coast",      -20.0, -40.0, "fast"),
    ("Hawaii",             19.7, -156.0, "slow, 8-10yr"),
    ("N. Atl deep-water",  60.0, -30.0, "poor ~0.4"),
]
COMPANIES = [
    ("Ebb Carbon",     48.1, -123.0, "Electrochemical OAE"),
    ("Planetary",      44.6, -63.6,  "Electrochemical OAE"),
    ("Vesta",          36.2, -75.75, "Mineral OAE"),
    ("Captura",        19.7, -156.0, "DOC (physics-exempt)"),
    ("Equatic",         1.3, 103.8,  "DOC (physics-exempt)"),
    ("SeaO2",          52.0, 4.3,    "DOC (physics-exempt)"),
    ("Gigablue",      -35.0, -160.0, "Iron fertilization"),
    ("Running Tide",   63.0, -20.0,  "Marine biomass sinking"),
    ("Carboniferous",  27.0, -91.0,  "Terrestrial burial (control)"),
]


def table(rows, kind):
    out = []
    for name, lat, lon, note in rows:
        r = {"site": name, "lat": lat, "lon": lon, "note": note}
        for H in (1, 5, 10):
            mean, lo, hi, snap = atlas_fkin(lat, lon, H)
            r[f"fkin_{H}yr"] = round(mean, 2)
            if H == 5:
                r["fkin_5yr_seasonrange"] = f"{lo:.2f}-{hi:.2f}"
                r["snap_deg"] = round(snap, 1)
        out.append(r)
    df = pd.DataFrame(out)
    print(f"\n=== {kind}: atlas f_kin (season-averaged) ===")
    print(df.to_string(index=False))
    return df


vdf = table(VALIDATION, "VALIDATION vs He & Tyka")
cdf = table(COMPANIES, "COMPANY DEPLOYMENTS")
cdf.to_csv(os.path.join(OUT, "atlas_fkin.csv"), index=False)
print("\nsaved -> outputs/atlas_fkin.csv")
