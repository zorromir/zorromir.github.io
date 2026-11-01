#!/usr/bin/env python3
"""Dependency-free source checks for the portfolio website."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
css = (ROOT / "styles.css").read_text(encoding="utf-8")
js = (ROOT / "app.js").read_text(encoding="utf-8")

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.pages = []
        self.links = []
        self.assets = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "article" and a.get("data-page"):
            self.pages.append((a["data-page"], a.get("aria-labelledby")))
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.images.append(a)
            self.assets.append(a.get("src", ""))
        if tag == "script" and a.get("src"):
            self.assets.append(a["src"])
        if tag == "link" and a.get("rel") == "stylesheet":
            self.assets.append(a["href"])

site = SiteParser()
site.feed(html)
expected = ["home", "projects", "research", "engineering", "about", "cv"]
assert [name for name, _ in site.pages] == expected, "Unexpected page order/routes"
assert len(site.ids) == len(set(site.ids)), "Duplicate element IDs"
assert all(label in site.ids for _, label in site.pages), "Page heading missing"
assert all("alt" in img for img in site.images), "Missing image alt text"
assert len(site.images) >= 6, "Project/research images missing"

for reference in site.links + site.assets:
    if reference.startswith("#"):
        assert reference[1:] in site.ids, f"Broken hash link: {reference}"
    elif reference.startswith(("https://", "http://", "mailto:", "data:")):
        continue
    else:
        path = reference.split("#", 1)[0].split("?", 1)[0]
        assert path and (ROOT / path).is_file(), f"Missing local asset: {reference}"

for marker in ("Paul Zegeling", "Monte Carlo", "The Fractional Harmonic Oscillator",
               "schoutenkelvin@gmail.com", "Synthetic reproduction shown"):
    assert marker in html, f"Expected scientific context missing: {marker}"
assert not re.search(r"98%|95%|WIREFRAME / CONCEPT|lorem ipsum", html, re.I)

assert 'class="research-finance-figure"' in html
assert "assets/empirical-finance-fit.svg" in html
# Recruiters must see evidence links without a hidden or unverified code claim.
assert html.count('class="home-feature-card"') == 2
assert html.count('class="home-feature-actions"') == 2
assert "https://github.com/zorromir/pipeline-flow-modelling" in html
assert "https://github.com/zorromir/fractional-harmonic-oscillator" in html
assert "projects/empirical-finance/README.md" in html
assert "https://github.com/zorromir/Empirical-Finance" in html
assert "ROBUSTNESS_RESULTS_2026-11-01.md" in html
assert "four of five industries" in html
assert "independent public python reconstruction" in html.lower()
assert "AI-assisted reconstruction" in html
assert "not predictive accuracy against company measurements" in html
assert "ILLUSTRATIVE DATA — NOT EMPIRICAL RESULTS" not in html
kernel = (ROOT / "assets/research/03_caputo_memory_kernel.svg").read_text(encoding="utf-8")
assert "<svg" in kernel and kernel.count("<path") >= 3, "Memory-kernel figure absent"
assert html.count("data-project-carousel") == 2
assert "data-paper-carousel" in html and "data-paper-filters" in html
assert "aria-current" in js and "aria-expanded" in js and "inert" in js
assert "fetch('data/reading-list.json')" in js
assert "prefers-reduced-motion" in css and "--layout-gutter" in css
assert css.count("{") == css.count("}"), "Unbalanced stylesheet blocks"
reading = json.loads((ROOT / "data/reading-list.json").read_text(encoding="utf-8"))
assert reading["papers"] and reading["categories"] and reading["projects"]
assert all(p.get("title") and p.get("url", "").startswith("https://") for p in reading["papers"])


# Phase 3: the editorial homepage uses isolated CSS and keeps evidence prominent.
home_css_path = ROOT / "home-editorial.css"
assert home_css_path.is_file(), "Missing Phase 3 homepage CSS"
home_css = home_css_path.read_text(encoding="utf-8")
assert "home-editorial.css?v=editorial-phase3-20261101" in html
assert 'class="shell explore-hero home-editorial-hero"' in html
assert '<h1 id="home-title">Mathematical modelling<br>&amp; quantitative finance.</h1>' in html
for expected_heading in (
    '<h2 id="home-featured-title">Selected projects</h2>',
    '<h2 id="home-research-title">Mathematics of memory</h2>',
    '<h2 id="home-current-title">Reading &amp; ongoing work</h2>',
):
    assert expected_heading in html, f"Editorial homepage heading missing: {expected_heading}"
assert "home-method-line" not in html, "Redundant promotional callout still present"
assert home_css.count("{") == home_css.count("}"), "Unbalanced homepage CSS blocks"
assert all(sel in home_css for sel in (
    "#home .home-editorial-hero",
    "#home .home-feature-grid",
    "#home .home-research-figure",
    "@media (max-width: 960px)",
    "@media (max-width: 810px)",
    "@media (max-width: 620px)",
    "@media (prefers-reduced-motion: reduce)",
)), "Missing homepage layout or accessibility rule"
assert "Synthetic reproduction shown" in html
assert "Historical, in-sample analysis" in html
print("PASS: Phase 3 editorial homepage headings, evidence links and responsive stylesheet.")

print(f"PASS: {len(site.pages)} pages, {len(site.images)} images, anchors, scientific figures, data and responsive styles.")
print("NOTE: Browser viewport tests, external URLs and CV personal details need manual review.")
