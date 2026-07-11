# Customize the investability model

Everything the model assumes about each carbon-removal method lives in one file:
[`src/priors.py`](src/priors.py). It is written to be edited by non-authors. If you think a
number should be different — because you have data, or an innovation that changes the economics
— change it there and re-run. Nothing else needs to be touched.

## The model in one line
```
realized_fraction = efficiency * (1 - lca_penalty)     # conditional on issuance
net_cost          = gross_cost / realized_fraction     # USD per creditable tonne
investable at price P  iff  net_cost < P
```
Plus a separate near-term issuance probability (does anyone actually pay you yet), which is the
dominant real-world gate today.

## The three levers you control (per method, in `src/priors.py`)
- **`cost_p10 / cost_p90`** — gross cost, USD per nominal tonne, at scale (10th–90th percentile).
- **`lca_p10 / lca_p90`** — lifecycle-emissions penalty: the fraction of removal eaten by the
  energy, materials, transport and process emissions of running the method. Per-method drivers and
  energy intensities are tabulated in `paper/APPENDICES.md` Appendix B.1.
- **`eff_*`** — realized-removal efficiency. For OAE it comes from the published ocean atlas at your
  lat/lon (`eff_kind="atlas_oae"`); for biological methods it is a method prior (`eff_kind="pathway"`);
  for physics-exempt methods it is 1 (`eff_kind="exempt"`).

## Worked example: an innovation that halves grinding energy (Mineral OAE)
Grinding energy drives both cost and the LCA penalty for mineral OAE. In `src/priors.py`:
```python
METHODS["Mineral OAE"].lca_p10  = 0.02   # was 0.03
METHODS["Mineral OAE"].lca_p90  = 0.06   # was 0.12
METHODS["Mineral OAE"].cost_p90 = 120    # was 165
METHODS["Mineral OAE"].note     = "grinding energy halved (OurCo process X)"
```
Then run `python build_v2.py` (or the Screener). Breakeven site-efficiency and P(investable) update.

## Add a brand-new method
Copy any `Method(...)` block in `METHODS`, give it a new name, set its numbers and `eff_kind`.

## Check your edits
`python src/priors.py` runs `validate()` and prints any problem (p10<p90, fractions in [0,1], etc.).

## What we will NOT let a number hide
The point of the model is honesty about the funnel. If you make a method look investable by
editing a prior, the assumption is now explicit and sourced in `note`/`source`, so a reader can
argue with it. That is the intended use: bring your own numbers, in the open.
