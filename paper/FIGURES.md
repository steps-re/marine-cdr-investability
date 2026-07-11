# Figure set — Nature Climate Change format

All figures share one style (`sim/ncc_style.py`): colorblind-safe palette (Okabe-Ito derived),
consistent sans typography, 300 dpi PNG for review + vector PDF for submission, Nature column widths.
Rendered to `outputs/figs_ncc/`.

| Fig | File | Source | Status |
|-----|------|--------|--------|
| 1 | `fig1_schematic` | `sim/fig1_schematic_v2.py` (no data) | **done** (base; illustrator final pass) |
| 2 | `fig2_region_result` | `e_campaign_global.csv` | **done** |
| 3 | `fig3_robustness` | `coarsen_bracket.csv`, `acc_window_sweep.csv` | **done** |
| 4 | `fig4_cross_model` | `e_campaign_global.csv`, `enatl_gs_fperm.csv` | **done** |
| 5 | `fig5_global_penalty` | `global_penalty_grid.npz` | **done** |
| 6 | `fig6_flushing_global` | `global_flushing_v3.nc` (native 1/12° flushing) | **done** |
| S1 | `figS1_predictors` | `s1_predictors.csv` (f_perm vs MLD/∇b/EKE, all weak) | **done** |
| S2 | `figS2_cross_model_wexchange` | `phase_e2_llc4320.csv`, `enatl_check.csv` | **done** |

All main + supplementary figures are rendered (300 dpi PNG + vector PDF). The only remaining figure task is an
illustrator's final art pass on the Fig 1 schematic; every data figure is submission-ready.

## Captions (draft)

**Fig 1 | The equilibration–subduction race, and why crediting-scale models miss it.**
(a) Added alkalinity draws down atmospheric CO2 only while the treated water stays in contact with the
air, over an equilibration time τ_eq of months to a year. At an ocean front, submesoscale motions subduct
that water below the mixed layer in days to weeks (τ_sub). When τ_sub < τ_eq the water is stranded before
it can equilibrate. (b) The fronts that do this are a few kilometres wide; coarsening the ocean to the ~100 km
resolution of the crediting efficiency atlases removes the resolved subduction almost entirely.

**Fig 2 | Fraction of treated surface water subducted below the winter mixed layer, by region.**
Lagrangian permanent-subduction fraction f_perm (native 2 km LLC4320), 14 regions, points and 95%
bootstrap confidence intervals. Open-ocean fronts and deep-convection sites strand 16–38%; enclosed,
shallow, and ice-covered basins strand ≈0. Colour encodes regime.

**Fig 3 | The signal is resolution-dependent and integration-robust.**
(a) Permanent subducted fraction versus model resolution (ACC box): the enhancement collapses toward zero
as the model is coarsened to the crediting-atlas resolution (shaded). (b) Native versus coarsened f_perm
versus integration window; the native fraction is stable and the native–coarse gap persists.

**Fig 4 | The same front in two independent models.**
Permanent subducted fraction at the Gulf Stream front in LLC4320 (MITgcm, ~2 km) and eNATL60 (NEMO,
~1.7 km), native versus coarsened to ~25 km. Two models built on different numerics reproduce a material
native fraction that the coarse field does not see. Error bars are 95% bootstrap CIs.

**Fig 5 | Where crediting-scale efficiency is most over-counted.**
(a) Modelled OAE efficiency (Zhou atlas). (b) Near-term subduction penalty from the regime model (open-ocean
median applied where the winter mixed layer is deep, ramped to zero in shallow/enclosed/ice basins).
(c) Efficiency after the penalty. The over-count concentrates in the subpolar North Atlantic and Pacific,
Nordic Seas, and Southern Ocean; of order 10–20% globally across the atlas ocean.

## What still needs a designer
Fig 1 is a clean, overlap-free matplotlib base. A Nature schematic is normally redrawn by an illustrator;
hand off `fig1_schematic.pdf` with this caption for a final art pass (typeface unification with the journal,
subtle depth shading, vector cleanup). Figs 2–5 are data figures and are submission-ready as vector PDF.
