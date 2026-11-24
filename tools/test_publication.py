import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
spec = importlib.util.spec_from_file_location("publication", Path(__file__).with_name("verify-publication.py"))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "build"
        self.src = Path(self.tmp.name) / "source"
        for path, html in {
            "field-notes/index.html": '<h1>Field Notes</h1><a href="/field-notes/new/">New</a>',
            "field-notes/new/index.html": '<h1>New</h1><a href="/field-notes/">Archive</a>',
        }.items():
            for root in (self.root, self.src):
                file = root / path
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text('<html><head><title>Test</title><link rel="stylesheet" href="/assets/atmosphere.css?v=1"></head><body>'+html+'</body></html>')
        for path, content in {"index.html":"home", "assets/atmosphere.css":"Shared Field Notes publication components", "assets/artist-node-architecture.svg":"svg", "source-version.json":'{"source_commit":"source"}'}.items():
            f = self.root / path
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(content)
    def build(self):
        return v.prepare(self.root, self.src, "source", "wrapper")
    def test_dynamic_route_and_metadata(self):
        manifest = self.build()
        self.assertIn("/field-notes/new/", manifest["files"])
        self.assertIn(v.ORIGIN+"/field-notes/new/", (self.root/"sitemap.xml").read_text())
        self.assertIn("BreadcrumbList", (self.root/"field-notes/new/index.html").read_text())
    def test_missing_article_fails(self):
        (self.root/"field-notes/new/index.html").unlink()
        with self.assertRaises(ValueError):
            self.build()
    def test_archive_omission_fails(self):
        f = self.root/"field-notes/index.html"
        f.write_text(f.read_text().replace('/field-notes/new/', '/'))
        with self.assertRaises(ValueError):
            self.build()
    def test_live_stale_content_fails(self):
        manifest = self.build()
        def fake(path):
            if path == "/publication-manifest.json":
                return json.dumps(manifest).encode()
            if path == "/field-notes/new/":
                return b"stale"
            return (self.root / (path.lstrip("/") + ("index.html" if path.endswith("/") else ""))).read_bytes()
        with patch.object(v, "fetch", side_effect=fake), self.assertRaisesRegex(ValueError, "Live content mismatch"):
            v.live(expected=manifest)
