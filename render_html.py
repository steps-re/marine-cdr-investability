"""
Render MANUSCRIPT + APPENDICES + REFERENCES into a single self-contained, NCC-styled
HTML with figures embedded as base64. Output: paper/manuscript.html
"""
import os, base64, re
import markdown

HERE = os.path.dirname(__file__)
PAPER = os.path.join(HERE, "paper"); OUTP = os.path.join(HERE, "outputs")

FIG_AT = {  # anchor text (in manuscript) -> figure file, caption
    "fig_schematic": ("fig_schematic.png", "Figure 1. The cashed-versus-stranded mechanism, in plain terms. A carbon-removal intervention makes surface seawater hungry for CO2; that hunger is satisfied only as CO2 crosses from air to sea over months to a year. If the treated water stays at the surface it is refilled by the atmosphere (cashed, left, green); if currents subduct it below the mixed layer first, the deficit is stranded in the deep ocean for years to centuries (right, red). Horizontal mixing spreads the signal but conserves the total, so dilution is not the loss; vertical export is. Right panel: realized removal (f_kin) rises toward the chemistry ceiling if equilibration outruns subduction, or freezes low if it does not."),
    "fig_overlay_atlas_v2": ("fig_overlay_atlas_v2.png", "Figure 2 (corrected). Net cost per creditable tonne versus atlas efficiency, conditional on verification, after removing the double-counted chemistry ceiling. OAE deployments plotted at their atlas f_kin; DOC and terrestrial burial are physics-exempt (flat); biomass and iron sit far above the market band."),
    "fig_investable_area_v2": ("fig_investable_area_v2.png", "Figure 3 (corrected). Fraction of the open ocean investable per method versus credit price, CONDITIONAL ON VERIFICATION, with 10-90 uncertainty bands. Mineral OAE clears most of the ocean above ~$150-200 (median) but with wide bands; biomass and iron are 0% everywhere."),
    "fig_issuance_risk_v2": ("fig_issuance_risk_v2.png", "Figure 4. The dominant near-term gate: probability a project actually gets credits issued, by pathway. Only Planetary has ever issued mCDR credits; ~0.3% of contracted volume issued. This multiplies conditional investability down to low-single-digit unconditional probabilities."),
    "fig_eez_bars": ("fig_eez_bars.png", "Figure 5. National EEZ mean 5-yr efficiency, colored by investment level. Chile (0.32) invests where its waters are least favorable; the best-endowed EEZs are largely uninvested. Small-sample EEZs are indicative only."),
    "fig_eez_map": ("fig_eez_map.png", "Figure 5b. Global choropleth of EEZ mean efficiency with engineered-mCDR investors marked."),
    "fig_carbonate_envelope": ("fig_carbonate_envelope.png", "Figure 6. Carbonate ceiling and safe-dose envelope per site (Appendix A.7 i). Left: the attainable-efficiency ceiling eta_max, higher in cold water. Right: aragonite saturation versus instantaneous alkalinity dose; the steeper warm-water curves hit the runaway threshold (Omega=5) far sooner, capping the per-deployment dose."),
    "fig_delivery_risk": ("fig_delivery_risk.png", "Figure 7. Delivery-risk: mean realized removal with its interannual P10-P90 spread across forcing years 2011-2020 (Appendix A.7 ii). Wide bars / high CV mark sites whose year-to-year delivery an offtaker must underwrite; absolute levels are monthly-forced and biased low, so the spread is the signal."),
    "fig_mrv_plume": ("fig_mrv_plume.png", "Figure 8. Site-level MRV verifiability from the real dispersing plume (Appendix A.7 iii): detectable window x containment -> implied issuance probability. Low everywhere, marginally best in contained settings; verification is the binding gate at site resolution."),
    "fig_season_sweep": ("fig_season_sweep.png", "Figure 9. Deployment-timing sweep (Appendix A.7 iv): realized removal by release quarter. Large seasonal swings at some sites (dose into the deep winter mixed layer, not the summer lid), negligible at deep-mixing sites."),
}


def img_tag(fname, caption):
    p = os.path.join(OUTP, fname)
    if not os.path.exists(p):
        return f'<p><em>[missing figure: {fname}]</em></p>'
    b64 = base64.b64encode(open(p, "rb").read()).decode()
    return (f'<figure><img src="data:image/png;base64,{b64}"/>'
            f'<figcaption>{caption}</figcaption></figure>')


def load(name):
    return open(os.path.join(PAPER, name)).read()


body_md = load("MANUSCRIPT.md")
# insert figures after the Figures list heading
fig_html = "\n\n".join(img_tag(f, c) for f, c in FIG_AT.values())
body_md = body_md.replace("## Figures", "## Figures\n\n" + fig_html + "\n\n### Figure captions\n")
full_md = body_md + "\n\n---\n\n" + load("APPENDICES.md") + "\n\n---\n\n" + load("REFERENCES.md")

html_body = markdown.markdown(full_md, extensions=["tables", "fenced_code", "toc", "sane_lists"])

CSS = """
body{font-family:Georgia,'Times New Roman',serif;max-width:820px;margin:40px auto;padding:0 24px;
line-height:1.55;color:#1a1a1a;font-size:17px}
h1{font-size:30px;line-height:1.2;margin-top:0.2em;border-bottom:2px solid #222;padding-bottom:8px}
h2{font-size:23px;margin-top:1.7em;color:#111;border-bottom:1px solid #ddd;padding-bottom:4px}
h3{font-size:19px;margin-top:1.3em;color:#333}
p{margin:0.7em 0}
em{color:#333}
table{border-collapse:collapse;width:100%;margin:1.2em 0;font-size:14px;font-family:-apple-system,Helvetica,Arial,sans-serif}
th,td{border:1px solid #bbb;padding:6px 9px;text-align:left;vertical-align:top}
th{background:#f0f0f0}
tr:nth-child(even){background:#fafafa}
figure{margin:1.5em 0;text-align:center}
figure img{max-width:100%;border:1px solid #ddd;border-radius:4px}
figcaption{font-size:14px;color:#555;margin-top:8px;text-align:left;font-family:-apple-system,Helvetica,Arial,sans-serif}
code{background:#f4f4f4;padding:1px 4px;border-radius:3px;font-size:14px}
hr{border:none;border-top:2px solid #eee;margin:2.5em 0}
a{color:#0a5}
.banner{background:#f7f9f7;border:1px solid #cde;border-radius:6px;padding:10px 16px;font-size:14px;
font-family:-apple-system,Helvetica,Arial,sans-serif;color:#345;margin-bottom:24px}
"""

BANNER = ('<div class="banner"><strong>Draft for review — Steps Ventures.</strong> '
          'Physics + data pipeline and figures generated on Google-for-Startups cloud credits; '
          'facts passed an independent grounded adversarial check (Appendix H). '
          'Interactive screener: <a href="https://marine-cdr-screener-582896243925.us-central1.run.app">live tool</a>.</div>')

html = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>Can the ocean cash the check? — Marine CDR investability</title>"
        f"<style>{CSS}</style></head><body>{BANNER}{html_body}</body></html>")

out = os.path.join(PAPER, "manuscript.html")
open(out, "w").write(html)
print("saved", out, "size(KB)=", round(os.path.getsize(out) / 1024, 1))
