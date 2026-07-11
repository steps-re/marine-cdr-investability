"""
global_flushing_v3.py — a TRUSTWORTHY, native-resolution global surface-residence field.
================================================================================================

WHAT THIS COMPUTES
------------------
For every ocean release cell on a global grid, how long does a patch of surface water stay put
before currents flush it away? We release parcels, advect them on real (eddying) daily currents,
and define the residence (flushing) time from the fraction still within a fixed radius R of their
origin after T years:

        tau_flush = -T / ln( fraction_still_within_R_after_T_years )     [years]

Fast-flushing shelves and through-flows give short tau; sheltered gyre interiors and enclosed
recirculations give long tau. This is a physically consistent, single-definition field: the SAME
R, T and parcel count are used at every point on Earth (unlike the earlier per-site diagnostic,
which used bespoke, differently-sized boxes and is therefore NOT comparable across sites).

WHY v3 (the honest history)
---------------------------
- v1 used monthly-climatology currents (no eddies) -> 96% of cells floored. Wrong.
- v2 used daily currents but coarsened to 1/4 deg, which smooths out the recirculation that
  produces retention -> still ~97% floored. Wrong.
- v3 advects on NATIVE 1/12 deg daily currents (eddies resolved), tiled so the native field fits
  in memory. A native regional test de-floored completely (0% floored), confirming resolution was
  the cause. This runs that native method for the whole ocean.

HOW IT STAYS WITHIN MEMORY (tiling)
-----------------------------------
The native global field (uo,vo, 1/12 deg, daily, 1 yr) is ~50 GB, too big for RAM. So we process
the ocean in TILE_DEG x TILE_DEG tiles. Each tile loads only its own native sub-field PLUS a HALO
buffer (so parcels can advect out of the interior before we count them flushed; HALO must exceed a
few flushing radii). Only the tile INTERIOR cells are recorded; the halo is discarded. Results are
saved per-tile (resumable: re-running skips finished tiles), then stitched into one global NetCDF.

EDIT ME (for outside users)
---------------------------
Every knob is in the PARAMETERS block below, with units and meaning. Change them and re-run:
  * R_KM      — the footprint that defines "still here" (deployment/verification scale).
  * YEARS     — the horizon over which residence is measured.
  * REL_DEG   — release-grid spacing (finer = more cells = slower).
  * PER_CELL  — parcels per cell (more = smoother fraction, slower).
  * TILE_DEG / HALO_DEG — memory-vs-edge-accuracy trade-off (bigger halo = safer, slower).
  * COARSEN   — 1 = native 1/12 deg (recommended). 2 = 1/6 deg (faster, loses some eddies).
Run: python sim/global_flushing_v3.py            (full global run; resumable)
     python sim/global_flushing_v3.py --stitch   (assemble finished tiles into the global NetCDF)
Output: sim/out/global_flushing_v3.nc  +  sim/out/gf_v3_tiles/*.npz (per-tile, for resume)
"""
import os, glob, gc, sys, traceback, subprocess
from datetime import timedelta
import numpy as np
import pandas as pd
import xarray as xr

# NOTE ON MEMORY: parcels leaks memory across repeated FieldSet/execute calls, so processing all
# tiles in ONE process accumulates until the OS OOM-kills it. We therefore run each tile in its
# OWN subprocess (main() orchestrates; `--tile LAT LON` runs exactly one tile and exits, freeing
# all memory). Slower per tile (fresh interpreter) but robust for an unattended multi-hour run.

# ============================== PARAMETERS (edit freely) ==============================
R_KM = 150.0          # residence radius: a parcel within this distance of origin is "still here"
YEARS = 2             # measurement horizon (years)
REL_DEG = 1.0         # release-grid spacing (deg)
PER_CELL = 12         # parcels released per cell
TILE_DEG = 20.0       # interior size of each processing tile (deg)
HALO_DEG = 6.0        # halo buffer loaded around each tile (deg); must be >> R_KM (~1.3 deg)
COARSEN = 1           # 1 = native 1/12 deg advecting field (recommended); 2 = 1/6 deg
DT_HOURS = 6          # advection timestep
LAT_MIN, LAT_MAX = -78.0, 80.0
# ======================================================================================

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data"); OUT = os.path.join(HERE, "out")
TILES = os.path.join(OUT, "gf_v3_tiles")
FLOOR_FRAC, CAP_FRAC = 1e-3, 0.999


def _ren(ds):
    r = {}
    if "latitude" in ds.coords: r["latitude"] = "lat"
    if "longitude" in ds.coords: r["longitude"] = "lon"
    return ds.rename(r)


def _open_lazy():
    files = sorted(glob.glob(os.path.join(DATA, "glob_cur_2019_*.nc")))
    if not files:
        sys.exit("no glob_cur_2019_*.nc daily-current files in sim/data/")
    return _ren(xr.open_mfdataset(files, combine="by_coords")).squeeze()


def _tile_id(lat0, lon0):
    return f"t_{int(round(lat0)):+04d}_{int(round(lon0)):+04d}"


def run_tile(ds, lat0, lon0, days_period):
    """Compute tau_flush for the interior cells of one tile. Returns (lon, lat, tau) arrays or None."""
    la0, la1 = lat0, lat0 + TILE_DEG
    lo0, lo1 = lon0, lon0 + TILE_DEG
    sub = ds.sel(lat=slice(la0 - HALO_DEG, la1 + HALO_DEG), lon=slice(lo0 - HALO_DEG, lo1 + HALO_DEG))
    if "depth" in sub.dims:
        sub = sub.isel(depth=0)
    u = sub["uo"]; v = sub["vo"]
    if COARSEN > 1:
        u = u.coarsen(lat=COARSEN, lon=COARSEN, boundary="trim").mean()
        v = v.coarsen(lat=COARSEN, lon=COARSEN, boundary="trim").mean()
    u = u.load(); v = v.load()
    if u.lat.size < 5 or u.lon.size < 5:
        return None
    ocean = np.isfinite(u.isel(time=0)).astype(float)
    if float(ocean.sum()) < 4:
        return None                                    # land-only tile
    u = u.where(np.isfinite(u), 0.0).astype("float32")
    v = v.where(np.isfinite(v), 0.0).astype("float32")
    tv = pd.to_datetime(u.time.values)

    # interior release grid
    glon = np.arange(lo0 + REL_DEG / 2, lo1, REL_DEG)
    glat = np.arange(max(la0, LAT_MIN) + REL_DEG / 2, min(la1, LAT_MAX), REL_DEG)
    if glon.size == 0 or glat.size == 0:
        return None
    LON, LAT = np.meshgrid(glon, glat)
    om = ocean.interp(lat=("z", LAT.ravel()), lon=("z", LON.ravel()), method="nearest").values
    keep = np.nan_to_num(om, nan=0.0) > 0.5
    clon = LON.ravel()[keep]; clat = LAT.ravel()[keep]
    if clon.size == 0:
        return None
    cid = np.arange(clon.size)
    rlon = np.repeat(clon, PER_CELL); rlat = np.repeat(clat, PER_CELL); rid = np.repeat(cid, PER_CELL)
    rng = np.random.default_rng(0)
    plon = rlon + rng.normal(0, REL_DEG * 0.12, rlon.size)
    plat = rlat + rng.normal(0, REL_DEG * 0.12, rlat.size)

    from parcels import FieldSet, ParticleSet, AdvectionRK4, JITParticle, Variable, StatusCode
    fds = xr.Dataset({"U": u, "V": v})
    fs = FieldSet.from_xarray_dataset(
        fds, {"U": "U", "V": "V"}, {"lon": "lon", "lat": "lat", "time": "time"},
        time_periodic=timedelta(days=float(days_period)))

    class P(JITParticle):
        cid = Variable("cid", dtype=np.int32, initial=0)

    def Kill(particle, fieldset, time):
        if particle.state == StatusCode.ErrorOutOfBounds:
            particle.delete()

    pset = ParticleSet(fs, pclass=P, lon=plon, lat=plat, cid=rid.astype(np.int32))
    pset.execute([AdvectionRK4, Kill], runtime=timedelta(days=365 * YEARS),
                 dt=timedelta(hours=DT_HOURS), verbose_progress=False)

    scid = np.array(pset.cid, dtype=int); selon = np.array(pset.lon); selat = np.array(pset.lat)
    o_lon = clon[scid]; o_lat = clat[scid]
    dist = np.sqrt(((selat - o_lat) * 111.0) ** 2 + ((selon - o_lon) * 111.0 * np.cos(np.radians(o_lat))) ** 2)
    win = dist < R_KM
    within = np.bincount(scid[win], minlength=clon.size)      # denominator = PER_CELL released
    frac = np.clip(within / PER_CELL, FLOOR_FRAC, CAP_FRAC)
    tau = -YEARS / np.log(frac)
    del u, v, fds, fs, pset; gc.collect()
    return clon, clat, tau


def one_tile(lat0, lon0):
    """Run exactly one tile in this process and save its npz, then exit (called via --tile)."""
    os.makedirs(TILES, exist_ok=True)
    out = os.path.join(TILES, _tile_id(lat0, lon0) + ".npz")
    if os.path.exists(out):
        return
    ds = _open_lazy()
    tv = pd.to_datetime(ds["time"].values); days_period = float((tv[-1] - tv[0]).days)
    try:
        r = run_tile(ds, lat0, lon0, days_period)
        if r is None:
            np.savez(out, lon=np.array([]), lat=np.array([]), tau=np.array([]))
        else:
            np.savez(out, lon=r[0], lat=r[1], tau=r[2])
            print(f"  {_tile_id(lat0, lon0)}: {r[0].size} cells, median tau {np.median(r[2]):.2f}yr", flush=True)
    except Exception:
        print(f"  {_tile_id(lat0, lon0)} FAILED:\n{traceback.format_exc()}", flush=True)


def main():
    """Orchestrate: run each unfinished tile in its OWN subprocess (memory-safe), then stitch."""
    os.makedirs(TILES, exist_ok=True)
    lat_starts = np.arange(np.floor(LAT_MIN / TILE_DEG) * TILE_DEG, LAT_MAX, TILE_DEG)
    lon_starts = np.arange(-180, 180, TILE_DEG)
    todo = [(la, lo) for la in lat_starts for lo in lon_starts]
    print(f"{len(todo)} candidate tiles; R={R_KM}km T={YEARS}yr native(coarsen={COARSEN}) "
          f"rel={REL_DEG} per_cell={PER_CELL}; one subprocess per tile", flush=True)
    for k, (la, lo) in enumerate(todo):
        if os.path.exists(os.path.join(TILES, _tile_id(la, lo) + ".npz")):
            continue                                          # resume: skip finished tiles
        print(f"[{k+1}/{len(todo)}] {_tile_id(la, lo)} ...", flush=True)
        subprocess.run([sys.executable, os.path.abspath(__file__), "--tile", str(la), str(lo)],
                       check=False)
    stitch()


def stitch():
    lons, lats, taus = [], [], []
    for f in sorted(glob.glob(os.path.join(TILES, "*.npz"))):
        z = np.load(f)
        if z["lon"].size:
            lons.append(z["lon"]); lats.append(z["lat"]); taus.append(z["tau"])
    if not lons:
        sys.exit("no tile results to stitch")
    clon = np.concatenate(lons); clat = np.concatenate(lats); tau = np.concatenate(taus)
    lo_u = np.unique(np.round(clon / REL_DEG) * REL_DEG); la_u = np.unique(np.round(clat / REL_DEG) * REL_DEG)
    grid = np.full((la_u.size, lo_u.size), np.nan)
    for i in range(clon.size):
        grid[np.argmin(np.abs(la_u - clat[i])), np.argmin(np.abs(lo_u - clon[i]))] = tau[i]
    da = xr.DataArray(grid, coords={"lat": la_u, "lon": lo_u}, dims=["lat", "lon"], name="tau_flush_yr")
    da.attrs.update(R_KM=R_KM, YEARS=YEARS, method="native-1/12deg daily-current Lagrangian residence",
                    definition="tau = -YEARS/ln(frac within R_KM of origin after YEARS)")
    da.to_netcdf(os.path.join(OUT, "global_flushing_v3.nc"))
    v = tau[np.isfinite(tau)]
    print(f"\n=== global_flushing_v3.nc: {v.size} cells ===")
    print(f"floored(<0.3yr) {100*(v<0.3).mean():.1f}%  retentive(>5yr) {100*(v>5).mean():.1f}%")
    print("quantiles yr:", np.round(np.quantile(v, [0, .1, .25, .5, .75, .9, .99, 1]), 2))


if __name__ == "__main__":
    if "--stitch" in sys.argv:
        stitch()
    elif "--tile" in sys.argv:
        i = sys.argv.index("--tile")
        one_tile(float(sys.argv[i + 1]), float(sys.argv[i + 2]))
    else:
        main()
