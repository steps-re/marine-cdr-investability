# Techno-Economic + LCA Priors for the Investability Engine

## Core identity
cost_net ≈ cost_gross / (f_kin × yield × (1-lambda_LCA) × nu_MRV). Energy-intensive, low-efficiency methods
compound badly. Best published demonstration: Ward et al. 2025 (OIF) cost swings $25 -> $53,000/tCO2 by varying
efficiency terms alone (doi:10.3389/fclim.2025.1509367). f_kin anchor: He & Tyka 2023 (realized 0.2-0.85 vs
nominal ~0.8) + Tyka 2025 (doi:10.5194/bg-22-341-2025).

## THE INVESTABILITY SPLIT (confirms the 2-axis model)
- PHYSICS-INSENSITIVE (cost roughly fixed, near-field MRV): terrestrial biomass burial (control), DOC/DIC
  stripping (Captura; carbon removed at outfall, measurable).
- PHYSICS-SENSITIVE (cost_net inflates as f_kin falls, MRV haircut grows far-field): mineral OAE, electrochemical
  OAE, marine biomass sinking, iron fertilization (EXTREME), artificial upwelling (EXTREME, net can be <0).

## Priors by archetype (cost $/tCO2 current->at-scale; energy; LCA penalty; yield; MRV; f_kin-sensitivity)
1. MINERAL OAE: modeled $20-200 (olivine ~$24-165), real 2024 offtake ~$270. Energy 224-748 kWh/t (olivine,
   grinding-dominated). LCA 14-223 kg/t (grain-size dep), ~51 (~5%) at 10um base (Foteinis 2023
   doi:10.1021/acs.est.2c08633). Yield 1.25 tCO2/t forsterite -> ~0.3-0.8 after gamma_AT(0.43-1.0)x0.8 air-sea.
   MRV far-field, CarbonPlan VCL 1-3, no fixed haircut. Sensitivity HIGH. Viability contested (Hangx&Spiers 2009
   centuries vs Foteinis fine-grain optimism).
2. ELECTROCHEMICAL OAE (Ebb, Planetary): ~$272 realized -> <$100 target, ~$50-160 at scale. Energy ~650-1850
   kWh/t (BPED). MRV BEST-QUANTIFIED: Isometric total deduction 14.35% on Planetary (interannual 8.90% + air-sea
   flux 6.51% dominate; LCA 5.27%; +2% buffer). CarbonPlan VCL 3. Sensitivity HIGH. Only realized uptake credited
   (>50% to date, full in 10-15 yr).
3. DOC / DIC STRIPPING (Captura, Equatic): stripping >$350; electrolytic mineralization ~$100-150; Captura target
   ~$100. Energy ~380 kWh/t (full H2 credit) to >2500; Equatic 1.9 MWh/t w/o H2 -> 0.38 w/ H2. Equatic 4.6 kg
   CO2/m3, ~29 kg H2/tCO2, ~59% DIC extraction. MRV NEAR-FIELD MEASURABLE at outfall = smallest haircut. Sensitivity
   LOW (removes C directly, equilibration-independent). Cost driver = seawater pumping.
4. MARINE BIOMASS SINKING (kelp; Running Tide defunct Jun2024): NASEM top-down $25-125 vs bottom-up $480-17,048
   (median ~$1,257). DeAngelo 2023 "never <$400/tCO2 unless removal fraction >0.6" (doi:10.1038/s41477-022-01305-9)
   = cleanest cost prop 1/f_kin statement. Baseline loses ~61% gross (628->244 credits, Coleman 2022). Bach 2021:
   atmospheric refill 2.5-18x longer than surface residence, efficacy cut 20-100% (contested, Bellamy/Boyd rebuttal).
   Removal frac 0.4-0.75. MRV: no accepted methodology, VCL 1-2, discount effectively unbounded. Sensitivity HIGH.
5. TERRESTRIAL BIOMASS BURIAL (crop residue/wood -> anoxic basin) = CONTROL: wood vault ~$14/t (Zeng 2022
   doi:10.1186/s13021-022-00202-0); Carboniferous ocean all-in UNDISCLOSED ("$1/t" = pilot rhetoric). Yield 1.6
   tCO2e/t dry; ~100% retained anoxic; <5% loss/3775yr (Zeng 2024 Science doi:10.1126/science.adm8133). f_kin
   STORAGE-limited not equilibration-limited = physics-insensitive BY CONSTRUCTION. MRV smallest surface (mass +
   retention); live question is additionality/leakage. Status: Carboniferous EPA permit 2026, not commercial.
6. IRON FERTILIZATION: NASEM <$50 (low conf); Ward 2025 $180-205 NOAK but full range $25-53,000; Harrison $457.
   Iron cheap; cost = efficiency+MRV driven. Only ~2% of new biomass durably stored (nutrient robbing 7% + 75%
   never exports + 85% ventilation + N2O 5%). Export 1-50%; EIFEX worked, LOHAFEX failed (3 of 12 showed
   sequestration). Long-term uptake <0.5. MRV worst-in-class (far-field, +3-4x). Sensitivity EXTREME (net can be <=0).
7. ARTIFICIAL UPWELLING: NASEM $100-150 low-conf. Net-negative risk CENTRAL: Oschlies 2010 ~80% of benefit is land
   cooling not ocean uptake, pumping high-DIC water may net OUTGAS; outcomes span <0 to +3.6 PgC/yr; collapses to
   0.32 under RCP2.6 (Jurchott 2023). No sea trial documented sequestration. Sensitivity EXTREME.

## Cross-method reference (for cross-check)
NASEM 2022 Table S.1: iron<$50; upwelling/OAE >$100-150; seaweed ~$100; electrochemical >$150. IPCC AR6 WG3
Table 12.6: OAE $40-260, ocean fert $50-500, EW $50-200, DACCS $100-300 (all TRL 1-2 for ocean). Fuss 2018 EW
$50-200. IEA DAC modeled $125-335 vs observed $500-1900 (modeled-vs-real gap afflicts mCDR too). Renforth &
Henderson 2017 EW $20-600, realized 1.4-1.7 mol CO2/cation.

## MRV difficulty ranking (haircut hierarchy)
DOC/DIC stripping (outfall-measured) ~ terrestrial burial (mass) > electrochemical OAE (VCL3, 14.35%) > mineral
OAE (VCL1-3) > marine biomass (VCL1-2, no method) > iron fert ~ upwelling (model-only, +3-4x or Fail).
Frameworks: CarbonPlan VCL 1-5; Frontier/[C]Worthy abiotic rubric (Omega_A>=7 runaway threshold, "no direct means
to measure"=Fail); Isometric OAE Protocol v1.0.

## f_kin physics core
eta_CO2 ~0.8 (0.75-0.85), ~0.79 Equator -> ~0.90 poles. tau_gas 3-9 mo; residence 2-20 wk; after 1yr realized eta
0.2-0.85 across sites; downwelling (Iceland) loses ~50% (realized ~0.4); plateau 2-4yr (Hawaii 8-10yr). Zhou&Tyka
2024 atlas (source.coop/cworthy/oae-efficiency-atlas). Revelle ~8-16 (subtropics 8-9, high-lat 13-15).

## DATA-QUALITY FLAGS (state in paper)
1. NASEM Table S.1 MRV column = verification DIFFICULTY ("High"=harder); verify header vs PDF before print.
2. Renforth&Henderson "0.8 air-sea" unverified in paywall; anchor 0.8 to He&Tyka 2023 / Tyka 2025 instead.
3. Kelp cost spans 100x ($25-17,000) -- always present range + removal-fraction dependence, never one number.
4. Iron fert has no defensible central cost; pair range with Ward $25-53,000 as efficiency-blowup illustration.
5. Company kWh/t undisclosed (Ebb/Planetary/Captura/Equatic) -- all energy = route-level envelopes not plant data.
6. Terrestrial ocean-sinking (Carboniferous) all-in cost + LCA absent -- genuine gap; only wood vault (~$14) published.
7. No accepted macroalgae-sinking methodology -- MRV discount unbounded (itself the finding).

## Strongest citation pair for cost=gross/efficiency thesis
Ward et al. 2025 (OIF $25->$53,000, doi:10.3389/fclim.2025.1509367) + He & Tyka 2023 (OAE realized 0.2-0.85 vs
nominal 0.8, doi:10.5194/bg-20-27-2023).
