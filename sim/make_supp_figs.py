"""
Supplementary figures S1 + S2 (NCC style).
S1: measured f_perm vs winter MLD, |grad b|, EKE across regions (all weak -> not parameterizable).
S2: submesoscale vertical-exchange enhancement in two independent models (LLC4320 vs eNATL60).
Run: .venv/bin/python sim/make_supp_figs.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ncc_style as S

S.apply()
DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")


def r2(x, y):
    A = np.polyfit(x, y, 1); p = A[0] * x + A[1]
    ss = np.sum((y - p) ** 2); tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - ss / tot if tot > 0 else 0.0


def fig_s1():
    df = pd.read_csv(os.path.join(DATA, "s1_predictors.csv"))
    preds = [("winter_MLD_m", "Winter mixed-layer depth (m)", "a"),
             ("gradb_1e8", "Front strength |∇b| (×10⁻⁸ s⁻²)", "b"),
             ("EKE_1e3", "Eddy kinetic energy (×10⁻³ m² s⁻²)", "c")]
    fig, ax = plt.subplots(1, 3, figsize=(S.COL2, 3.1))
    for a, (col, xl, letter) in zip(ax, preds):
        d = df.dropna(subset=[col])
        fit = d[d.role == "fit"]; hold = d[d.role == "holdout"]
        a.scatter(hold[col], hold.f_perm, s=32, c=S.REGIME["null"], edgecolor="white", linewidth=0.5, label="holdout", zorder=3)
        a.scatter(fit[col], fit.f_perm, s=36, c=S.PALETTE["native"], edgecolor="white", linewidth=0.5, label="fit fronts", zorder=4)
        R = r2(fit[col].values, fit.f_perm.values)
        a.text(0.95, 0.95, f"R² = {R:.2f}", transform=a.transAxes, ha="right", va="top",
               fontsize=8.5, color=S.PALETTE["warn"], weight="bold")
        a.set_xlabel(xl); a.set_ylim(-0.02, 0.42)
        if letter == "a":
            a.set_ylabel("Permanent subducted fraction  $f_{\\mathrm{perm}}$")
            a.legend(loc="lower right", fontsize=7)
        S.panel_label(a, letter)
    fig.suptitle("The subduction bias is not parameterizable from coarse fields (every predictor is weak)", y=1.02)
    fig.tight_layout()
    S.save(fig, "figS1_predictors")


def fig_s2():
    llc = pd.read_csv(os.path.join(DATA, "phase_e2_llc4320.csv")).iloc[0]
    en = pd.read_csv(os.path.join(DATA, "enatl_check.csv")).iloc[0]
    groups = [("Vertical velocity\n(w RMS enhancement)",
               (llc.w_enhance_x, llc.w_enhance_ci_lo, llc.w_enhance_ci_hi),
               (float(en.w_enhance), None, None)),
              ("Downward flux\n(gross enhancement)",
               (llc.flux_enhance_x, llc.flux_enhance_ci_lo, llc.flux_enhance_ci_hi),
               (float(en.flux_enhance), None, None))]
    fig, ax = plt.subplots(figsize=(S.COL1, 3.6))
    x = np.arange(len(groups)); w = 0.36
    for i, (nm, l, e) in enumerate(groups):
        yerr_l = [[l[0] - l[1]], [l[2] - l[0]]] if l[1] is not None else None
        ax.bar(x[i] - w / 2, l[0], w, yerr=yerr_l, capsize=3, color=S.PALETTE["native"],
               label="LLC4320 (MITgcm)" if i == 0 else None)
        ax.bar(x[i] + w / 2, e[0], w, color=S.PALETTE["coarse"], label="eNATL60 (NEMO)" if i == 0 else None)
    ax.axhline(1.0, ls=":", lw=1, color=S.PALETTE["neutral"])
    ax.set_xticks(x); ax.set_xticklabels([g[0] for g in groups], fontsize=7.5)
    ax.set_ylabel("Native ÷ coarsened enhancement (×)")
    ax.set_ylim(0, 3.4); ax.grid(axis="x", visible=False)
    ax.legend(loc="upper right", fontsize=7.5)
    ax.set_title("Submesoscale vertical exchange in two independent models", loc="left")
    S.save(fig, "figS2_cross_model_wexchange")


if __name__ == "__main__":
    fig_s1()
    fig_s2()
    print("done: figS1, figS2 ->", S.OUT)
