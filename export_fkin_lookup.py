"""
Export a compact global f_kin lookup from the atlas for the Cloud Run screener,
so the app ships a few-MB npz instead of the 677 MB source netCDF.
Saves season-mean OAE efficiency at 1/5/10 yr on the POP grid + coords + valid mask.
"""
import os
import numpy as np
import xarray as xr

HERE = os.path.dirname(__file__)
ds = xr.open_dataset(os.path.join(HERE, "data", "OAE_efficiency_maps_alltime.nc"))
eff = ds["OAE_efficiency"].values          # (season, N_month, nlat, nlon)


def seasonmean(month_idx):
    return np.nanmean(eff[:, month_idx, :, :], axis=0).astype("float32")


fk1, fk5, fk10, fk15 = seasonmean(11), seasonmean(59), seasonmean(119), seasonmean(179)
# per-season 5-yr stack for uncertainty (season spread)
fk5_seasons = ds["OAE_efficiency"].values[:, 59, :, :].astype("float32")  # (season, nlat, nlon)
valid = np.isfinite(fk5)
out = os.path.join(HERE, "app", "fkin_lookup.npz")
os.makedirs(os.path.dirname(out), exist_ok=True)
np.savez_compressed(
    out,
    tlat=ds["TLAT"].values.astype("float32"),
    tlong=ds["TLONG"].values.astype("float32"),
    fk1=fk1, fk5=fk5, fk10=fk10, fk15=fk15, fk5_seasons=fk5_seasons, valid=valid,
)
print("saved", out, "size(MB)=", round(os.path.getsize(out) / 1e6, 2),
      "| valid cells:", int(valid.sum()))
