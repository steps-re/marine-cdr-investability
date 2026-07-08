# Can the ocean cash the check? An air–water equilibration filter for marine and aquatic CDR investment

A physics-based due-diligence screen for marine/aquatic carbon-dioxide-removal (CDR) investment. It overlays
real company and national deployment geographies onto the published global ocean-alkalinity-enhancement (OAE)
efficiency atlas, plus a reduced-form Monte-Carlo investability model, to ask **where** removal is physically
and economically realizable and **whether** it can be certified.

**Live artifacts:** formatted paper + PDF and an interactive investability screener (links in `paper/MANUSCRIPT.md`).

## Headline findings
- Almost all marine CDR realizes *atmospheric* removal only via slow, location-dependent air–water CO₂ exchange.
  The binding physical loss is **vertical subduction of the treated water before it equilibrates** (cashed vs.
  stranded), not horizontal dilution.
- **Conditional on verification:** mineral OAE is broadly investable above ~$150–250/t (wide uncertainty),
  electrochemical OAE above ~$250; marine biomass sinking (~25% realized efficiency) and iron fertilization
  (~2%) are uninvestable at any price to $500/t. Direct ocean capture and terrestrial burial are physics-exempt.
- **The dominant near-term gate is verification, not physics or cost:** only one project has ever had mCDR
  credits issued (~0.3% of contracted volume issued), so every pathway has a low-single-digit-percent
  unconditional chance of being paid today.
- Several nations with active programs (most sharply Chile, mean EEZ efficiency 0.32) invest where their own
  waters are least favorable; the best-endowed coasts are largely uninvested.

## Reproduce
```bash
python -m venv .venv && source .venv/bin/activate
pip install numpy pandas scipy xarray netCDF4 'PyCO2SYS>=1.8,<2' matplotlib geopandas shapely pyproj markdown
# 1) download the efficiency atlas (Zhou et al. 2024 / [C]Worthy), then:
python export_fkin_lookup.py     # derive the compact f_kin lookup (app/fkin_lookup.npz, included)
python build_v2.py               # corrected investability model + figures + tables -> outputs/
python make_schematic.py         # Figure 1 (cashed vs stranded)
python eez_aggregate.py          # national EEZ figure (needs Marine Regions EEZ shapefile)
python render_html.py            # assemble paper/manuscript.html
```
`src/investability_v2.py` is the corrected model; `src/model.py` is the reduced-complexity emulator (consistency
check). `app/` is the deployable Streamlit screener.

## Data sources (third-party; not redistributed here)
- **OAE efficiency atlas:** Zhou et al. 2024, *Nature Climate Change*, doi:10.1038/s41558-024-02179-9; open data
  at source.coop/cworthy/oae-efficiency-atlas.
- **EEZ boundaries:** Marine Regions (VLIZ), marineregions.org.
- **Deployment-geography dataset** (compiled here): `outputs/*.csv` and `literature/02,04,06,07`.
- Techno-economic and efficiency priors: see `paper/APPENDICES.md` B and `literature/05,08` (with DOIs).

## Corrections of record (post-review)
The model was corrected after an adversarial multi-reviewer pass: (1) the atlas efficiency already embeds the
~0.8 carbonate ceiling, so it is the sole OAE location-efficiency term (no double-counted yield); (2) biological
and iron pathways use their own realized-removal efficiency, not the OAE atlas; (3) uncertainty bands, multiple
horizons, correlated cost/LCA priors, and a binary MRV issuance gate were added. See `paper/APPENDICES.md` H.

## Competing interests
Compiled by Steps Ventures, an investment entity with a potential interest in marine-CDR outcomes. All priors
and code are released here so readers can inspect and reproduce every result. Analysis reuses third-party
published data. Not investment advice.

## License
Code: MIT (`LICENSE`). Text/figures: CC-BY-4.0.
