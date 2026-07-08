# Marine CDR & Air-Sea Equilibration: Physics and Literature Landscape

*Compiled July 2026 by research agent. Key correction: tau_eq = (h/k)*(R_ion/R_f) —
Revelle factor in the DENOMINATOR; net CO2 slowdown vs inert gas is R_ion/R_f (~10-20x).*

## Key verified references
- **Jones, Ito, Takano & Hsu (2014)** "Preformed..." *Global Biogeochemical Cycles* 28(11):1163-1178,
  doi:10.1002/2014GB004813. Equilibration timescale: global median ~4.1 mo, mean ~4.4 mo, SD ~3.4 mo,
  range <1 mo to ~2 yr. tau negatively correlated with k and Revelle, positively with MLD and ionization fraction.
- **He & Tyka (2023)** "Limits and CO2 equilibration of near-coast alkalinity enhancement,"
  *Biogeosciences* 20:27-43, doi:10.5194/bg-20-27-2023. eta_CO2 = dDIC/dAlk. 17 near-coast sites (MITgcm/ECCO).
  After 1 yr eta 0.2-0.85; plateau 0.6-0.8 by 3-4 yr; theoretical max ~0.8. Fast: Brazil, Madagascar, Peru,
  Tasmania, Kerguelen, Patagonia. Slow: Hawaii (8-10 yr). Poor: N. Atlantic deep-water stalls ~0.4 after 20 yr.
- **Zhou, Tyka, Ho, Yankovsky, Bachman, Nicholas, Karspeck & Long (2024)** "Mapping the global variation in
  the efficiency of ocean alkalinity enhancement for carbon dioxide removal," *Nature Climate Change* 15:59-65,
  doi:10.1038/s41558-024-02179-9. FIRST global time-resolved OAE efficiency map. 690 pulse patches x 4 seasons,
  CESM2 1 deg. Downloadable atlas: source.coop/cworthy/oae-efficiency-atlas; explainer carbonplan.org/research/oae-efficiency-explainer.
- **Yamamoto, DeVries & Siegel (2024)** "Metrics for quantifying the efficiency of atmospheric CO2 reduction by mCDR,"
  *Environmental Research Letters* 19(10):104053, doi:10.1088/1748-9326/ad7477. Cumulative additionality alpha and
  relative efficiency epsilon vs DAC. OAE alpha rises 0->40-90% over years-decades; epsilon->~100% only after ~40 yr.
- **Nowicki, DeVries & Siegel (2024)** "Influence of Air-Sea CO2 Disequilibrium on Carbon Sequestration by the
  Biological Pump," *GBC* 38 e2023GB007880, doi:10.1029/2023GB007880. Disequilibrium adds ~75 yr (near-surface) to
  >600 yr (Southern Ocean/N. Atlantic) to sequestration time. Supports thesis for biological pathway.
- **Renforth & Henderson (2017)** "Assessing ocean alkalinity for carbon sequestration," *Rev. Geophysics* 55:636-674,
  doi:10.1002/2016RG000533. Foundational OAE review.
- **NASEM (2022)** *A Research Strategy for Ocean-based CDR and Sequestration*, doi:10.17226/26278. Six pathways;
  durable-storage bar ~1000+ yr; air-sea equilibration + MRV flagged as central gaps.
- **Egleston, Sabine & Morel (2010)** "Revelle revisited," *GBC* 24 GB1002, doi:10.1029/2008GB003407. Buffer factors.
- **Wanninkhof (1992)** *JGR* 97(C5):7373, doi:10.1029/92JC00188; **(2014)** *L&O Methods* 12:351,
  doi:10.4319/lom.2014.12.351: k = 0.251<U^2>(Sc/660)^-0.5 cm/hr, ~20% uncertainty.
- **Siegel, DeVries, Doney & Bell (2021)** *ERL* 16:104003, doi:10.1088/1748-9326/ac0be0. Sequestration timescales.
- **Bach (2024)** "The additionality problem of OAE," *Biogeosciences* 21:261-277, doi:10.5194/bg-21-261-2024.
- **Zhou et al. (2025)** *Biogeosciences* 22:341-353, doi:10.5194/bg-22-341-2025. Efficiency metrics responsive vs prescribed pCO2.
- TO-CONFIRM bylines: Wang et al., Burt et al., Fennel/Ho MRV chapter (State of the Planet 2-oae2023).

## Novelty (model level)
No published study does a global Monte Carlo across ALL mCDR pathways ranking them by local air-sea
equilibration efficiency with propagated uncertainty. Existing maps are single deterministic runs, OAE-only
(Zhou 2024) or biological-only (Nowicki 2024).

## Datasets (if ever needed) — but per Mike's steer we REUSE published fields, not rebuild
- Published efficiency atlas: Zhou 2024 (source.coop/cworthy/oae-efficiency-atlas). PRIMARY reuse target.
- Wind: CCMP v3.1, ERA5 (ARCO-ERA5 Zarr). MLD: de Boyer Montegut v2024 (SEANOE 10.17882/98226), Holte Argo.
- Carbonate: GLODAPv2.2016b gridded + PyCO2SYS 1.8.x. SST: OISST v2.1.
- pCO2/flux: SOCAT v2025 (validation), Landschutzer SOM-FFN, SeaFlux ensemble (6 pCO2 x 3 wind).
- Residence/subduction: derive from ECCO v4r4 or OCIM2 first-passage. No clean product.

## Efficiency metric definitions
- eta_CO2 = dDIC/dAlk (He & Tyka) — realized uptake per unit intervention; max ~0.8 tropics, ~0.9 high-lat.
- Cumulative additionality alpha (Yamamoto) — atmos reduction / perturbation; time-dependent.
- Relative efficiency epsilon = alpha_mCDR/alpha_DAC.
- Durability thresholds in literature: 1-10 yr (policy/crediting), 100 yr (market "durable"), 1000+ yr (NASEM).
