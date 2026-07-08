"""
Figure 1 - conceptual physics explainer for investment decision-makers.
Panel A: spatial 'cashed vs stranded' - a treated surface parcel either equilibrates
with the atmosphere in place (real removal) or is subducted below the mixed layer with
its CO2 deficit uncashed (stranded for years-centuries). Horizontal dilution is benign.
Panel B: realized fraction vs time - equilibration outruns subduction (cashed) or not (stranded).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Ellipse, Rectangle

fig, (axA, axB) = plt.subplots(1, 2, figsize=(15, 6.2), gridspec_kw={"width_ratios": [1.35, 1]})

# ---------- Panel A: spatial schematic ----------
axA.set_xlim(0, 12); axA.set_ylim(0, 10); axA.axis("off")
# layers
axA.add_patch(Rectangle((0, 7), 12, 3, facecolor="#eaf3fb", edgecolor="none"))      # atmosphere
axA.add_patch(Rectangle((0, 3.6), 12, 3.4, facecolor="#d5efe8", edgecolor="none"))   # mixed layer
axA.add_patch(Rectangle((0, 0), 12, 3.6, facecolor="#c9dcef", edgecolor="none"))     # deep ocean
axA.plot([0, 12], [7, 7], color="#3a7", lw=2)                                         # sea surface
axA.text(0.2, 9.3, "ATMOSPHERE", fontsize=11, weight="bold", color="#557")
axA.text(0.2, 6.5, "SURFACE MIXED LAYER  (in contact with air)", fontsize=10, weight="bold", color="#276")
axA.text(0.2, 3.0, "DEEP OCEAN INTERIOR  (out of contact, years-centuries)", fontsize=10, weight="bold", color="#357")
axA.text(6, 9.75, "How ocean carbon removal is realized - or lost", fontsize=13, weight="bold", ha="center")

# LEFT: cashed
axA.text(2.9, 8.55, "CASHED", fontsize=13, weight="bold", color="#1a7d3c", ha="center")
axA.add_patch(Ellipse((2.9, 5.3), 3.2, 1.5, facecolor="#bfe6c9", edgecolor="#1a7d3c", lw=1.5))
axA.text(2.9, 5.3, "treated parcel\n(low CO2)", fontsize=8.5, ha="center", va="center", color="#1a5")
for x in (1.9, 2.9, 3.9):                                                            # air->sea flux arrows
    axA.add_patch(FancyArrowPatch((x, 8.0), (x, 6.1), arrowstyle="-|>", mutation_scale=16,
                                  color="#1a7d3c", lw=2))
axA.annotate("horizontal mixing spreads\nbut conserves the total (fine)", (4.4, 5.3), (5.9, 5.75),
             fontsize=8, color="#487", ha="center", va="center",
             arrowprops=dict(arrowstyle="->", color="#487", connectionstyle="arc3,rad=-0.2"))
axA.text(2.9, 4.05, "atmosphere refills the deficit  =  REAL removal", fontsize=9, ha="center", color="#1a7d3c")

# RIGHT: stranded
axA.text(9.0, 8.55, "STRANDED", fontsize=13, weight="bold", color="#b1272b", ha="center")
axA.add_patch(Ellipse((9.0, 5.3), 2.6, 1.4, facecolor="#f2cfcf", edgecolor="#b1272b", lw=1.5))
axA.text(9.0, 5.3, "treated parcel\n(low CO2)", fontsize=8.5, ha="center", va="center", color="#a33")
# weak/aborted air-sea flux
axA.add_patch(FancyArrowPatch((8.2, 8.0), (8.2, 7.15), arrowstyle="-|>", mutation_scale=12, color="#c99", lw=1.5))
axA.text(8.05, 7.45, "x", fontsize=15, color="#b1272b", weight="bold")
# subduction arrow into the deep
axA.add_patch(FancyArrowPatch((9.6, 4.7), (10.4, 1.6), arrowstyle="-|>", mutation_scale=22, color="#b1272b", lw=2.6))
axA.text(11.2, 2.6, "subducted\nbefore\nequilibrating", fontsize=8.5, color="#b1272b", ha="center")
axA.text(9.0, 4.05, "deficit exported to depth  =  uncashed for decades+", fontsize=9, ha="center", color="#b1272b")
axA.text(6, 0.5, "The binding race:  air-sea equilibration time (months to ~1 yr)  vs.  surface residence before the water sinks",
         fontsize=9.5, ha="center", style="italic", color="#333")

# ---------- Panel B: realized fraction vs time ----------
t = np.linspace(0, 10, 300)
eta, tau_eq = 0.8, 1.2
f_cashed = eta * (1 - np.exp(-t / tau_eq))
axB.plot(t, f_cashed, color="#1a7d3c", lw=3, label="stays at surface: cashed")
# stranded: freezes at subduction time
tsub = 1.0
f_at_sub = eta * (1 - np.exp(-tsub / tau_eq))
f_str = np.where(t <= tsub, eta * (1 - np.exp(-t / tau_eq)), f_at_sub)
axB.plot(t, f_str, color="#b1272b", lw=3, label="subducts at ~1 yr: stranded")
axB.axvline(tsub, color="#b1272b", ls=":", lw=1.5)
axB.axhline(eta, color="#888", ls="--", lw=1)
axB.text(6.2, eta + 0.02, "chemistry ceiling  (~0.8)", fontsize=9, color="#555")
axB.annotate("subduction\nfreezes it here\n(f_kin ~ 0.4)", (tsub, f_at_sub), (2.4, 0.28),
             fontsize=9, color="#b1272b",
             arrowprops=dict(arrowstyle="->", color="#b1272b"))
axB.set_xlabel("years after intervention", fontsize=11)
axB.set_ylabel("realized atmospheric removal  (fraction of potential,  f_kin)", fontsize=10.5)
axB.set_title("Equilibration must outrun subduction", fontsize=13, weight="bold")
axB.set_ylim(0, 0.95); axB.set_xlim(0, 10); axB.grid(alpha=0.25); axB.legend(loc="lower right", fontsize=9.5)

fig.tight_layout()
fig.savefig("outputs/fig_schematic.png", dpi=150, bbox_inches="tight")
print("saved -> outputs/fig_schematic.png")
