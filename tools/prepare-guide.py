from pathlib import Path
import json
import subprocess

output = Path("upstream/tools/atmosphere-guide/dist/client")
index = output / "index.html"
html = index.read_text()
head = """<link rel="canonical" href="https://atmosphere.loptrlab.com/">
<meta name="description" content="Getting to Know the Atmosphere: a PIXIE field guide by Loptr Lab. Explore independent apps, portable identity and resources for learning, creating, publishing, connecting and building.">
<meta property="og:title" content="Getting to Know the Atmosphere — a PIXIE field guide by Loptr Lab">
<meta property="og:description" content="Explore the open social web at your own pace, with clear sources, creator ownership and room for understanding and cooperation.">
<meta property="og:url" content="https://atmosphere.loptrlab.com/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Loptr Lab">
<meta property="og:image" content="https://atmosphere.loptrlab.com/assets/atmosphere-orbit.jpg">
<meta property="og:image:alt" content="A violet orbit illustration accompanying the PIXIE Atmosphere field guide.">
<meta name="twitter:card" content="summary_large_image">
"""
index.write_text(html.replace("</head>", head + "</head>"))
(output / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://atmosphere.loptrlab.com/sitemap.xml\n")
(output / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://atmosphere.loptrlab.com/</loc></url></urlset>\n')
sha = subprocess.check_output(["git", "-C", "upstream", "rev-parse", "HEAD"], text=True).strip()
(output / "source-version.json").write_text(json.dumps({"source_repository": "ibloud/pixie-device-stewardship", "source_commit": sha, "source_path": "tools/atmosphere-guide"}, indent=2) + "\n")
assert "assets/atmosphere-orbit.jpg" in "".join(p.read_text() for p in (output / "assets").glob("*.js"))
assert (output / "assets/atmosphere-orbit.jpg").stat().st_size > 50000
assert (output / "assets/made-sick-icon.svg").stat().st_size > 0
print("Dedicated guide metadata and source provenance prepared.")
