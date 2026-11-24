"""Build and verify the Atmosphere Pages release. No third-party dependencies."""
import argparse
import hashlib
import json
import re
import time
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urljoin
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

ORIGIN = "https://atmosphere.loptrlab.com"
BASE = Path("upstream/tools/atmosphere-guide")
MANIFEST = "publication-manifest.json"
CSS = "/assets/atmosphere.css"

def require(condition, message):
    if not condition:
        raise ValueError(message)

class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.links, self.styles, self.canonicals, self.schemas = [], [], [], []
        self.title, self.h1 = [], []
        self.capture = None
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "link":
            rel = (a.get("rel") or "").split()
            if "stylesheet" in rel:
                self.styles.append(a.get("href", ""))
            if "canonical" in rel:
                self.canonicals.append(a.get("href", ""))
        if tag in ("h1", "title"):
            self.capture = tag
        if tag == "script" and a.get("type") == "application/ld+json":
            self.capture = "schema"
            self.schemas.append("")
        if tag == "nav":
            require("breadcrumb" not in (a.get("aria-label") or "").lower(), "Redundant visible breadcrumbs")
    def handle_endtag(self, tag):
        if tag in ("h1", "title", "script"):
            self.capture = None
    def handle_data(self, data):
        if self.capture == "schema":
            self.schemas[-1] += data
        elif self.capture in ("h1", "title"):
            getattr(self, self.capture).append(data)

def route(rel):
    return "/" + str(rel).removesuffix("index.html")

def digest(data):
    return hashlib.sha256(data).hexdigest()

def local_path(href, page_route):
    u = urlsplit(urljoin(ORIGIN + page_route, href))
    return u.path if u.scheme == "https" and u.netloc == urlsplit(ORIGIN).netloc else None

def prepare(root, source_root, source, wrapper):
    expected = {p.relative_to(source_root) for p in (source_root / "field-notes").rglob("index.html")}
    actual = {p.relative_to(root) for p in (root / "field-notes").rglob("index.html")}
    archive = Path("field-notes/index.html")
    require(archive in expected and len(expected) > 1, "Missing source archive or articles")
    require(expected == actual, f"Source/build route mismatch: {expected ^ actual}")
    routes = {route(p) for p in expected}
    for rel in sorted(expected):
        file = root / rel
        html = file.read_text(encoding="utf-8")
        page = Page(html)
        title = "".join(page.h1).strip()
        path = route(rel)
        require(title and "".join(page.title).strip(), f"Missing title: {rel}")
        require(any(local_path(s, path) == CSS for s in page.styles), f"Missing shared stylesheet: {rel}")
        canonical = ORIGIN + path
        require(not page.canonicals or page.canonicals == [canonical], f"Incorrect canonical: {rel}")
        if not page.canonicals:
            html = html.replace("</head>", f'<link rel="canonical" href="{escape(canonical)}"></head>', 1)
        crumbs = [("Loptr Lab", ORIGIN + "/"), ("Field Notes", ORIGIN + "/field-notes/")]
        if rel != archive:
            crumbs.append((title, canonical))
        schema = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                  "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "item": u}
                                      for i, (n, u) in enumerate(crumbs, 1)]}
        existing = [json.loads(s) for s in page.schemas]
        breadcrumbs = [s for s in existing if isinstance(s, dict) and s.get("@type") == "BreadcrumbList"]
        require(not breadcrumbs or breadcrumbs == [schema], f"Invalid or duplicate breadcrumb schema: {rel}")
        if not breadcrumbs:
            html = html.replace("</head>", '<script type="application/ld+json">' + json.dumps(schema).replace("<", "\\u003c") + "</script></head>", 1)
        links = {local_path(h, path) for h in page.links}
        for link in links:
            if link and link.startswith("/field-notes/"):
                require(link in routes, f"Broken Field Notes link: {rel}: {link}")
        if rel == archive:
            require(routes - {path} <= links, "Archive omits an article")
        else:
            require("/field-notes/" in links, f"Missing archive return link: {rel}")
        file.write_text(html, encoding="utf-8")
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    sitemap = ET.Element(f"{{{ns}}}urlset")
    for path in ["/"] + sorted(routes):
        ET.SubElement(ET.SubElement(sitemap, f"{{{ns}}}url"), f"{{{ns}}}loc").text = ORIGIN + path
    ET.ElementTree(sitemap).write(root / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    version = json.loads((root / "source-version.json").read_text())
    require(version.get("source_commit") == source, "Source provenance mismatch")
    require("Shared Field Notes publication components" in (root / CSS.lstrip("/")).read_text(), "Missing shared CSS components")
    paths = {"/": "index.html", CSS: CSS.lstrip("/"), "/sitemap.xml": "sitemap.xml", "/source-version.json": "source-version.json",
             "/assets/artist-node-architecture.svg": "assets/artist-node-architecture.svg"}
    paths.update({route(p): str(p) for p in expected})
    manifest = {"version": 1, "source_commit": source, "wrapper_commit": wrapper,
                "files": {url: digest((root / file).read_bytes()) for url, file in sorted(paths.items())}}
    (root / MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Verified {len(expected)-1} articles, archive, metadata, assets and provenance.")
    return manifest

def fetch(path):
    require(path.startswith("/") and not path.startswith("//"), "Invalid manifest URL")
    with urlopen(Request(ORIGIN + path, headers={"Cache-Control": "no-cache", "User-Agent": "LoptrLab-Publication-Verification"}), timeout=20) as response:
        require(urlsplit(response.geturl()).netloc == urlsplit(ORIGIN).netloc, "Unexpected redirect")
        require(response.status == 200, f"Unexpected status: {path}")
        return response.read()

def live(source=None, wrapper=None, expected=None):
    manifest = json.loads(fetch("/" + MANIFEST))
    require(manifest.get("version") == 1, "Unsupported manifest")
    if expected is not None:
        require(manifest == expected, "Live manifest differs from exact build")
    else:
        require(manifest.get("source_commit") == source and manifest.get("wrapper_commit") == wrapper, "Stale release")
    files = manifest["files"]
    require({"/", "/field-notes/", CSS, "/sitemap.xml", "/source-version.json"} <= files.keys(), "Incomplete manifest")
    require(any(p.startswith("/field-notes/") and p != "/field-notes/" for p in files), "No articles in manifest")
    for path, sha in files.items():
        require(digest(fetch(path)) == sha, f"Live content mismatch: {path}")
    print("Public release verified against manifest: " + manifest["source_commit"])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "live"])
    parser.add_argument("--source")
    parser.add_argument("--wrapper")
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--attempts", type=int, default=1)
    a = parser.parse_args()
    if a.mode == "build":
        require(a.source and a.wrapper, "Source and wrapper commits required")
        prepare(BASE / "dist/client", BASE / "public", a.source, a.wrapper)
    else:
        expected = json.loads(a.expected.read_text()) if a.expected else None
        for i in range(a.attempts):
            try:
                live(a.source, a.wrapper, expected)
                return
            except Exception as exc:
                print(f"Public verification attempt {i+1}: {exc}", flush=True)
                if i + 1 == a.attempts:
                    raise
                time.sleep(15)

if __name__ == "__main__":
    main()
