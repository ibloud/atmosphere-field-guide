from pathlib import Path
import json
import subprocess

output = Path("upstream/tools/atmosphere-guide/dist/client")
index = output / "index.html"
html = index.read_text()
head = """<link rel="canonical" href="https://atmosphere.loptrlab.com/">
<meta name="description" content="Getting to Know the Atmosphere: a Loptr Lab field guide. Explore independent apps, portable identity and resources for learning, creating, publishing, connecting and building.">
<meta property="og:title" content="Getting to Know the Atmosphere — a Loptr Lab field guide">
<meta property="og:description" content="Explore the open social web at your own pace, with clear sources, creator ownership and room for understanding and cooperation.">
<meta property="og:url" content="https://atmosphere.loptrlab.com/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Loptr Lab">
<meta property="og:image" content="https://atmosphere.loptrlab.com/assets/atmosphere-orbit.jpg">
<meta property="og:image:alt" content="A violet orbit illustration accompanying the Loptr Lab Atmosphere field guide.">
<meta name="twitter:card" content="summary_large_image">
"""
index.write_text(html.replace("</head>", head + "</head>"))
(output / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://atmosphere.loptrlab.com/sitemap.xml\n")
(output / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://atmosphere.loptrlab.com/</loc></url></urlset>\n')
sha = subprocess.check_output(["git", "-C", "upstream", "rev-parse", "HEAD"], text=True).strip()
(output / "source-version.json").write_text(json.dumps({"source_repository": "ibloud/pixie-device-stewardship", "source_commit": sha, "source_path": "tools/atmosphere-guide"}, indent=2) + "\n")
assert "assets/atmosphere-orbit.svg" in "".join(p.read_text() for p in (output / "assets").glob("*.js"))
assert (output / "assets/atmosphere-orbit.svg").stat().st_size > 0

# Keep layout rhythm on an 8px Material-style spacing scale and prevent the
# onboarding controls from stretching into oversized cards at tablet widths.
spacing_css = """
:root { --space-1: 8px; --space-2: 16px; --space-3: 24px; --space-4: 32px; }
.onboarding { padding: var(--space-3); margin-block: var(--space-2) var(--space-4); }
.start-options { gap: var(--space-2); margin-block: var(--space-3); }
.start-options button { min-height: 48px; padding: var(--space-2); }
.identity { padding: var(--space-3); margin-top: var(--space-4); }
.pathways { margin-top: var(--space-4); }
.resource-row { gap: var(--space-2) var(--space-3); padding: var(--space-3); margin-bottom: var(--space-2); }
.resource-action { gap: var(--space-2) var(--space-3); padding-top: var(--space-2); }
.made-sick { gap: var(--space-3); padding: var(--space-3); margin-top: var(--space-4); }
@media (max-width: 620px) {
  .onboarding, .identity, .resource-row, .made-sick { padding: var(--space-2); }
  .made-sick { gap: var(--space-2); }
}
"""
for css_file in output.glob("assets/*.css"):
    css_file.write_text(css_file.read_text() + spacing_css)
print("Dedicated guide metadata, source provenance, and consistent spacing prepared.")
