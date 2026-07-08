# Water-Body Taxonomy Synthesis (for the paper)

Distilled from literature/06 (comprehensive water-body scan) + 01-05. Organizing axes:
(A) WATER BODY, (B) atmosphere-COUPLED vs STORAGE-only, (C) physics-SENSITIVE vs EXEMPT (investability),
(D) is it RESOLVED by the global 1-deg ocean atlas (Zhou 2024)?

## CORRECTED FACTS (update from "verified ~0")
Verified, registry-issued aquatic-CDR credits now exist but are TRIVIALLY SMALL (~800 tCO2 total, 3 first-of-kind):
- Planetary Technologies 625.6 t — Ocean Alkalinity Enhancement (Isometric, Jun 2025; Halifax; ~$271/t Frontier).
- CREW Carbon 104.4 t — WASTEWATER Alkalinity Enhancement (Isometric WAE Protocol v1.2, early 2025; New Haven CT ->
  Long Island Sound; first-ever WAE credits; $32.1M Frontier offtake).
- CarbonRun 76.69 t — RIVER Alkalinity Enhancement (Isometric RAE Protocol, Jan 2026; Kvina River Norway -> North Sea;
  first-ever RAE credits; 55,442 t Frontier offtake 2025-29).
Everything else remains forward offtake. Delivered still ~2% of contracted. So: "verified is trivially small (hundreds
of tonnes across three first-of-kind projects), and even those were credited before/with partial equilibration."

## THE UNIVERSAL CAVEAT (paper strength)
The global 1-deg OCEAN atlas (Zhou 2024) resolves ONLY the open ocean. Every non-open-ocean water body
(marginal/semi-enclosed seas, estuaries/coastal, freshwater lakes, rivers, wastewater outfalls, aquifers, mine pit
lakes) is UNRESOLVED by it -- shorter residence, stronger stratification, lower/again-variable buffering, sharp
gradients -> the air-water filter STILL applies but is MORE model-dependent and MRV is harder. So the filter is
quantifiable where we can (open ocean) and a known-unknown everywhere else; the enclosed/freshwater cases are often
WORSE (stratified lids, outgassing) not better.

## TAXONOMY TABLE
| Water body | Coupled/Storage | Physics-sensitive? | Atlas-resolved? | Filter difference vs open ocean | Representative players |
|---|---|---|---|---|---|
| Open ocean | coupled (OAE, DOC, kelp, iron) + storage (terr. sinking) | mixed | YES (Zhou 2024) | baseline; tau_eq months->1yr | Ebb, Planetary, Captura, Equatic, Gigablue, Running Tide(defunct) |
| Marginal/semi-enclosed seas (Baltic, Black, North, Med, Caspian, Gulf) | coupled + storage | yes | NO | restricted exchange, strong stratification "lid", long residence, low-alk Baltic = high Revelle; Baltic legal ban (Helsinki Conv.) | Rewind (Black Sea BiCRS-storage), CaspianCDR (microalgae), CDRmare (North Sea/Baltic research) |
| Estuaries/coastal/fjords | coupled | yes | NO (too coarse; our snap-dist caveat) | high variability, freshwater stratification, tidal gas transfer, variable Revelle | most OAE/DOC pilots (Vesta, Ebb, Planetary Halifax) |
| Freshwater lakes / Great Lakes / reservoirs | coupled | yes | NO (saltwater model) | LOW buffering (Revelle high/variable) -> faster equilibration but TINY storage capacity; seasonal stratification | none operational; Vesta prospective; EPA/NOAA acidification monitoring |
| Rivers (river alkalinity enhancement) | coupled, equilibrates DOWNSTREAM at sea | yes (+ in-river outgassing loss) | NO | short residence; ~2/3 C can be lost to in-river carbonate precip/outgassing (16-27% less effective, UK study; <5% to >15% site-dependent) | CarbonRun (VERIFIED, Kvina), UNDO/Eion (land->river weathering) |
| Wastewater / industrial effluent | coupled, near-field measurable | LOW (point-source, measured) | NO (outfall) | engineered, measured inputs/outputs; upstream dosing cuts plant emissions too | CREW Carbon (VERIFIED WAE), UMCES research; Isometric WAE protocol |
| Desalination brine | coupled | LOW-med | NO | engineered intake/outfall; co-located; RMI ~30% infra cost saving | Equatic (Singapore/LA), Ebb, Planetary (co-locatable) |
| Groundwater / aquifer / mine pit lakes / tailings | mostly STORAGE (mineralization) or land-weathering->aquifer | exempt-ish (mineralization) / coupled (pit-lake OAE) | NO | soil-gas interface, very slow flow, or solid mineralization; pit lakes stratified | Arca (tailings, Microsoft ~300kt), Travertine, Exterra, Aquarry (pit-lake OAE), PNNL Wallula (basalt mineralization) |

## New/less-known players surfaced (not in 02)
Open ocean: Vycarb (NYC East River bicarbonate), Cestore (offshore-wind DOC), Carbon Time, Arbon Earth (bamboo OceanPods
kelp), XoIS (iron, Gulf of Alaska research). Marginal: Rewind, CaspianCDR. Rivers: CarbonRun, UNDO. Wastewater: CREW.
Tailings/mine: Arca Climate, Travertine, Exterra, Aquarry, Newmont-NREL REMineD.

## Registry protocols now spanning water bodies (Isometric leading)
OAE (coastal outfalls), Wastewater Alkalinity Enhancement (WAE v1.2), River Alkalinity Enhancement (RAE), Electrolytic
Seawater Mineralization, DOCS. All bake in an air-water uptake/equilibration term and a <1 efficiency ceiling. This is
the market ALREADY pricing the filter where it can -- and it can only do so with site-specific high-res models, NOT the
global atlas -> reinforces the "quantifiable only in open ocean, known-unknown elsewhere" point.

## HALLUCINATION GUARD
Gemini's scan wrongly asided that "Zhou et al. 2024 is on tidal channel formation." FALSE. Zhou, Tyka, Ho et al. 2024
Nature Climate Change (doi:10.1038/s41558-024-02179-9) IS the global OAE efficiency atlas (data downloaded from
source.coop/cworthy/oae-efficiency-atlas). Do NOT propagate the error.

## GLOBAL INVESTABLE-AREA HEADLINE (outputs/global_investable_area.csv)
% of open ocean clearing each method's breakeven vs price: Mineral OAE 0%(<=$150)/41%($200)/92%($250)/99%($350);
Electrochemical OAE 0%(<=$200)/12%($250)/79%($300)/94%($350); Marine biomass sinking & Iron fertilization = 0% at
EVERY price to $500. DOC + terrestrial burial physics-exempt (price-limited, not location-limited).
