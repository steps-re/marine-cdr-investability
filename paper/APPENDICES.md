# Appendices

## Appendix A — Methods in full

**A.1 Air–sea efficiency field.** We use the published global atlas of ocean-alkalinity-enhancement (OAE) efficiency (Zhou et al. 2024; open data at source.coop/cworthy/oae-efficiency-atlas), a CESM ocean–biogeochemistry ensemble of 690 alkalinity-release regions × 4 injection seasons, integrated 15 years. The archived field `OAE_efficiency(season, month, nlat, nlon)` is the cumulative atmospheric CO₂ uptake divided by alkalinity added, i.e. f_kin, on the model's curvilinear grid. We take the season mean at month 60 as the 5-year f_kin (and months 12, 120 for the 1- and 10-year horizons).

**A.2 Sampling at deployment coordinates.** For each project we find the nearest grid cell with a defined efficiency value (snapping coastal points to the nearest resolved ocean cell) and record the snap distance in degrees; snaps beyond ~1° are flagged as coarse. Validation sites reproduce He & Tyka (2023): Peru/Tasmania/Patagonia/Brazil 0.70–0.79 at 5 yr (fast); Hawaiʻi 0.59→0.72 (1→10 yr, slow-recovers); North Atlantic deep-water 0.50→0.52 (stalls).

**A.3 Reduced-complexity emulator (cross-check).** An independent box model computes τ_eq = (h/k)(R_ion/R_f) with k from Wanninkhof (2014) and R_f, R_ion from PyCO2SYS (Humphreys et al. 2022), and realized kinetic efficiency from the competition between τ_eq and a surface-residence prior. It reproduces the atlas/He–Tyka ordering (Fig. A1) and is used only as a transparent audit and to reason about unresolved water bodies. Planetary/Halifax lands at 0.62–0.64 (emulator and atlas), consistent with the published ~0.515 realized fraction for Halifax Harbour.

**A.4 Investability identity.** cost_net = cost_gross / (f_kin · η_yield · (1 − λ_LCA) · ν_MRV). For physics-exempt methods f_kin ≡ 1. The physics breakeven at price P is the minimum f_kin with P(cost_net < P) ≥ 0.5 under the Monte-Carlo priors (Appendix B), 8,000–20,000 draws.

**A.5 National aggregation.** We area-weight (cos φ) the 5-year f_kin over all resolved ocean cells within each sovereign EEZ (Marine Regions polygons, made valid and simplified to 0.1°), reporting means for EEZs with ≥20 cells. The 1° atlas resolves narrow coastal EEZs poorly (e.g. the United States retains only ~47 cells); small-sample means are flagged.

**A.6 Independent circulation cross-check (offline Lagrangian tracer).** To test whether our reading of the atlas is physically sound with *independent* inputs, we ran an offline three-dimensional tracer-transport model on a different data source than the atlas's embedded CESM: daily GLORYS12 reanalysis currents and mixed-layer depth (Copernicus Marine, 1/12°) plus CMEMS L4 wind-stress for Ekman pumping. Neutrally-buoyant parcels are advected in 3-D (OceanParcels, RK4); while a parcel is in the mixed layer it relaxes its CO₂ deficit at the local air–sea rate k·R_f/R_ion, and it is carried below by the resolved vertical velocity — continuity divergence plus Ekman pumping w_ek = −curl(τ/ρf). Permanent stranding is emergent, not imposed: a parcel that subducts below the winter-maximum mixed layer goes dormant and re-entrains only when winter convection or the circulation lifts it. Two features close the edge cases the earlier version missed: (i) **bathymetry** from GLORYS — where the seafloor is shallower than the winter mixed layer (shelf seas), the column ventilates fully and nothing strands; (ii) **Ekman pumping** — the actual permanent-subduction driver in subtropical gyres. The model is a consistency check and coastal/enclosed extension, not a new climate simulation; the atlas remains authoritative for the open ocean.

Five-year cashed fraction versus the atlas at sites spanning the regimes (800 parcels each):

| Site | Regime | Tracer f_kin (5 yr) | Atlas f_kin | Note |
|---|---|---|---|---|
| North Sea | shelf sea | 0.90 | 0.83 | bathymetry fix (seafloor < winter MLD → no stranding) |
| Halifax | temperate coastal | 0.67 | 0.62 | Planetary site |
| Salish Sea | fjord/estuary | 0.83 | 0.80 | |
| Iceland | subpolar, deep MLD | 0.50 | 0.47 | |
| Patagonia (Puerto Montt) | high-residence coastal | 0.93 | 0.70–0.79 | high (deep-fjord retention) |
| Hawaiʻi (Kona) | subtropical gyre | 0.31 | 0.59 | **under-predicts** — decadal re-emergence not captured in a 5-yr offline periodic-year run |

The circulation cross-check reproduces the atlas ordering and values across the temperate, coastal, subpolar and shelf regimes, and — unlike the emulator — uses fully independent circulation data, so it is a genuine (not circular) check on the open-ocean numbers. The one documented miss is the subtropical gyre (Hawaiʻi), where realized efficiency accrues over a decade-plus as subducted water slowly re-ventilates; a 5-year offline run under-counts it, and we defer to the atlas there. Within-EEZ maps built from the same model (`*_map3`) show the internal spatial gradient of realized removal for the eight most-invested national waters; they are consistent with the point sites (e.g. NZ 0.84, Chile coastal 0.86 on physical residence, Japan 0.50) but are coarse (1.5° release grid) and measure physical residence only, not the carbonate-outgassing penalty the atlas folds in (so, e.g., the Humboldt outgassing signal is an atlas/chemistry effect, not a residence effect).

**A.7 Investment-grade site metrics (offline-model extensions).** The mean cashed fraction is one number; investment decisions turn on risk, capacity, verifiability and timing. Four further metrics, all from the same GLORYS/CMEMS/PyCO2SYS pipeline, resolve those axes at the site level (Figs. 6–9).

*(i) Carbonate ceiling and safe-dose envelope (PyCO2SYS, per site).* The attainable efficiency ceiling η_max = dDIC/dTAlk at fixed atmospheric pCO₂ falls from ~0.88–0.89 in cold water (Halifax, Iceland, Black Sea) to ~0.81–0.82 in the warm subtropics (Kona, Singapore); true realized yield is residence-cashed × η_max. The safe instantaneous alkalinity dose before the aragonite saturation state passes the runaway-precipitation threshold (Ω_arag ≈ 5, which reverses removal) is ~290–310 µmol kg⁻¹ in cold water but only 120–160 in the warm subtropics, because the warm baseline Ω_arag (3.3–3.7) already sits close to runaway. Warm-water OAE therefore carries a much lower per-deployment capacity ceiling — a direct constraint on project scale and capital intensity that the efficiency field alone does not reveal.

*(ii) Delivery-risk (interannual variance).* Running the tracer on each forcing year 2011–2020 (monthly GLORYS) gives the year-to-year spread of realized removal — the delivery risk a buyer underwrites. The coefficient of variation ranges from 2.7% (Patagonia — near-constant delivery) and 8–10% (Black Sea, Halifax, Duck NC) to ~20–22% (Gulf of Maine, Singapore, Iceland, Kona). Monthly-mean currents lose the eddy field and bias the *absolute* level low relative to the daily/atlas-matched values, so we report the *spread* (CV, P10–P90), not the level. Two sites (North Sea, Black Sea) required an enlarged model domain: their default boxes were narrower than the water body itself, so parcels were deleted at the box edge while still in the sea; on the corrected domains they resolve to 0.70 (CV 20%) and 0.90 (CV 8%).

*(iii) MRV plume footprint → site-level issuance.* Tracking the real dispersing surface plume (detectable pCO₂-anomaly window × spatial containment) yields a verifiability score and an implied issuance probability *per site* rather than by archetype. Verifiability is low everywhere (0.18–0.25 → implied issuance 4–5%), marginally best in contained settings (Karsto fjord, 0.25). This reproduces the paper's central result — verification, not physics or cost, is the binding near-term gate — now at map resolution. The scores are a relative ranking; the short detectable windows are conservative.

*(iv) Deployment timing.* Sweeping the release month shows real operational alpha at some sites and none at others: Karsto gains 26 points of realized removal by dosing in April rather than October, and Kona 13 points by dosing in January, while deep-mixing Halifax is flat (~1 point). The rule is to dose into the deepening or deep winter mixed layer, not a shallow summer lid that subducts the anomaly.

These metrics are offline-model extensions and inherit its limits (monthly-forcing bias on absolute levels; regional retention; a reduced-form MRV signal); they are decision-support rankings, not bankable guarantees, and the atlas remains authoritative for absolute open-ocean efficiency.

## Appendix B — Techno-economic priors (per archetype)

Ranges are literature-anchored 10th–90th-percentile priors, at-scale (see REFERENCES). Cost = US$/nominal-tonne gross.

| Archetype | cost_gross ($/t) | LCA penalty λ | MRV survival ν | yield | physics-sensitive |
|---|---|---|---|---|---|
| Mineral OAE | 30–165 | 0.03–0.12 | 0.60–0.85 | 0.80 | yes (HIGH) |
| Electrochemical OAE | 60–200 | 0.04–0.15 | 0.78–0.90 | 0.80 | yes (HIGH) |
| Direct ocean capture / DIC stripping | 100–400 | 0.08–0.30 | 0.88–0.97 | 1.00 | no (exempt) |
| Marine biomass sinking | 400–3000 | 0.15–0.50 | 0.30–0.60 | 0.55 | yes (HIGH) |
| Terrestrial biomass burial (control) | 14–120 | 0.02–0.08 | 0.80–0.95 | 1.00 | no (exempt) |
| Iron fertilization | 100–2000 | 0.05–0.15 | 0.20–0.45 | 0.50 | yes (EXTREME) |

Key anchors: Renforth & Henderson 2017; Fuss 2018; Strefler 2018; Foteinis 2023 (coastal-OAE LCA); DeAngelo 2023 and Coleman 2022 (kelp cost ∝ 1/removal-fraction); Ward 2025 (iron fertilization US$25–53,000/t across efficiency terms); Isometric 14.35% uncertainty deduction on Planetary.

**Pathway efficiency priors (fixing M2; NOT the OAE atlas):** OAE uses the atlas f_kin directly (already includes the ~0.8 carbonate ceiling — no separate yield term, fixing M1). Marine biomass sinking: realized atmospheric-removal efficiency central ~25%, 10–90 range 5–40% (Bach 2021; DeAngelo 2023; Gao & Taylor 2024; qualitative point Hurd 2024). Iron fertilization: ~2% durably sequestered, 0.5–5% (Ward 2025; NASEM 2022). Priors sampled lognormally.

**Near-term binary issuance probability (from the recent record; Fig. 4):** mineral OAE 5–15%, electrochemical OAE 3–12%, DOC 1–5%, marine biomass <2%, iron fertilization <2%, terrestrial burial 5–25%. Basis: only Planetary has ever had mCDR credits issued; ~0.3% of ~578,000 t contracted issued as of 2025–26; MRV can exceed 50% of project cost; issuance lifecycle 3–5 yr. Cost↔LCA priors sampled with correlation ρ≈0.5 (energy-intensive → both higher).

## Appendix C — Water-body taxonomy

| Water body | Coupling | Physics-sensitive | Atlas-resolved | Filter difference vs open ocean | Representative players |
|---|---|---|---|---|---|
| Open ocean | coupled + storage | mixed | yes | baseline; τ_eq months→1 yr | Ebb, Planetary, Captura, Equatic, Gigablue, Running Tide (defunct) |
| Marginal/semi-enclosed seas | coupled + storage | yes | no | restricted exchange, stratified lid, low-alk Baltic; storage debated under Helsinki Conv. | Rewind (Black Sea, storage), CaspianCDR, CDRmare |
| Estuaries/coastal/fjords | coupled | yes | no | high variability, freshwater stratification, tidal gas transfer | Vesta, Ebb, Planetary (Halifax) |
| Freshwater lakes / Great Lakes | coupled | yes | no | low buffering → fast but tiny capacity | none operational; Vesta prospective |
| Rivers | coupled (equilibrates downstream) | yes + in-river loss | no | short residence; 16–27% loss to in-river precip/outgassing (UK study) | CarbonRun (verified), UNDO, Eion |
| Wastewater / effluent | coupled, near-field measured | low | no | engineered, measured; Isometric WAE protocol | CREW Carbon (verified), UMCES |
| Desal brine | coupled | low–med | no | engineered intake/outfall | Equatic, Ebb |
| Groundwater / mine tailings / pit lakes | storage (mineralization) or land→aquifer | mostly exempt | no | solid mineralization or slow flow | Arca, Travertine, Exterra, Aquarry, PNNL Wallula |

## Appendix D — Deployment overlay, corrected (conditional on verification, plus issuance gate)

`atlas f_kin` = OAE only (n/a for pathway methods, which use their own efficiency, fixing M2).
`P(clears|MRV)` = probability net cost < price *conditional on being certified*. `issuance` = near-term
binary probability of certification. `P(paid) uncond` ≈ P(clears|MRV @350) × issuance-midpoint.

| Company | Method | atlas f_kin (5yr) | P(clears@200 \| MRV) | P(clears@350 \| MRV) | issuance near-term | P(paid@350) uncond |
|---|---|---|---|---|---|---|
| Ebb Carbon | Electrochemical OAE | 0.80 | 0.71 | 0.96 | 3–12% | 0.072 |
| Planetary | Electrochemical OAE | 0.62 | 0.51 | 0.86 | 3–12% | 0.064 |
| Vesta | Mineral OAE | 0.59 | 0.73 | 0.92 | 5–15% | 0.092 |
| Captura | DOC / DIC stripping | 1.0 (exempt) | 0.36 | 0.73 | 1–5% | 0.022 |
| Equatic | DOC / DIC stripping | 1.0 (exempt) | 0.36 | 0.73 | 1–5% | 0.022 |
| SeaO2 | DOC / DIC stripping | 1.0 (exempt) | 0.38 | 0.75 | 1–5% | 0.022 |
| Gigablue | Iron fertilization | n/a (pathway) | 0.00 | 0.00 | 0–2% | 0.000 |
| Running Tide (defunct) | Marine biomass sinking | n/a (pathway) | 0.00 | 0.00 | 0–2% | 0.000 |
| Carboniferous | Terrestrial burial (control) | 1.0 (exempt) | 0.96 | 0.99 | 5–25% | 0.149 |

Every pathway has a low-single-digit-percent unconditional chance of being paid near-term: verification, not physics or cost, is the binding gate.

## Appendix E — National EEZ efficiency (5-yr, investing nations + notable extremes)

| Sovereign | Mean f_kin (5yr) | cells | Investment level |
|---|---|---|---|
| Ghana | 0.74 | – | none |
| Canada | 0.71 | 562 | engineered |
| Argentina | 0.70 | 206 | none |
| United Kingdom | 0.69 | 989 | engineered |
| Norway | 0.68 | 1070 | engineered |
| Netherlands | 0.68 | 40 | engineered |
| Iceland | 0.66 | 415 | blue-carbon/assess |
| Brazil | 0.63 | 520 | blue-carbon/assess |
| United States | 0.62 | 47 (coarse) | engineered |
| India | 0.49 | 133 | blue-carbon/assess |
| Chile | 0.32 | 311 | engineered |
| (top, uninvested) Guyana / Barbados | 0.83 | 20–27 | none |
| (top, uninvested) Uruguay | 0.80 | 32 | none |

## Appendix F — Global investable-area, CORRECTED (% of open ocean clearing breakeven, 5-yr, conditional on verification)

Median over correlated cost/LCA Monte-Carlo priors; 10–90 bands are wide (shown in Fig. 3). The old
(buggy) table double-counted the ~0.8 chemistry ceiling and biased these pessimistically; corrected values below.

| Method (median %) | $100 | $150 | $200 | $250 | $300 | $350 | $500 |
|---|---|---|---|---|---|---|---|
| Mineral OAE | 6 | 93 | 99 | 100 | 100 | 100 | 100 |
| Electrochemical OAE | 0 | 4 | 78 | 97 | 99 | 99.6 | 100 |
| Marine biomass sinking | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Iron fertilization | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Bands (10–90) span ~0–100% at intermediate prices — investability is dominated by cost/LCA uncertainty, not
physics. Multi-horizon (1/5/10/15-yr): OAE efficiency rises with horizon as subducted alkalinity re-emerges, so
5-yr is conservative for slow sites. Biomass and iron are 0% because pathway efficiency (~25%, ~2%) and gross
cost overwhelm siting. DOC and terrestrial burial are physics-exempt (price-limited, location-independent). All
figures here are CONDITIONAL on verification; the near-term issuance gate (Fig. 4) multiplies them down to
low-single-digit unconditional probabilities.

## Appendix G — Interactive screener

A Streamlit due-diligence tool (method + latitude/longitude → P(investable), physics breakeven, net-cost-vs-efficiency curve) is deployed on Cloud Run, drawing on the atlas lookup and the Appendix B priors. It lets any new deal be triaged against the filter.

## Appendix H — Adversarial accuracy check

Twelve load-bearing external claims were independently fact-checked with grounded search (skeptical by default). Outcomes: 4 CONFIRMED (US strategy ignores equilibration; river 16–27% loss; Isometric OAE/WAE/RAE protocols; Zhou 2024 = the OAE atlas), 8 PARTIALLY-CONFIRMED with corrections applied to the manuscript. Corrections of record: Planetary's 625.6 t was bought by Stripe/Shopify/British Airways (Frontier holds a separate 115,211 t offtake); the New Zealand "dumping" rejection was Oceaneos (iron fertilization, 2023), not Gigablue; CREW's $32.1 M covers a 71,878 t offtake, not the 104.4 t first batch; the delivered/contracted ratio is a fraction of a percent (~0.3% issued in one 2025 analysis); the Baltic storage "ban" is a contested interpretation of the Helsinki Convention; the Humboldt is outgassing-prone rather than an unconditional net source. Full log in `ADVERSARIAL_CHECK.md`.
