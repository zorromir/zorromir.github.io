#!/usr/bin/env python3
"""Dependency-free source checks for the portfolio website."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
css = (ROOT / "styles.css").read_text(encoding="utf-8")
editorial_css = (ROOT / "academic.css").read_text(encoding="utf-8")
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
def count_class(name):
    return sum(name in classes.split() for classes in re.findall(r'class="([^"]+)"', html))

assert count_class("home-feature-card") == 2
assert count_class("home-feature-actions") == 2
home = html.split("<!-- PAGE 1: HOME -->", 1)[1].split("<!-- PAGE 2: PROJECTS -->", 1)[0]
assert 'class="shell academic-home-intro"' in home
assert 'class="academic-home-work-list"' in home
assert "The Fractional Harmonic Oscillator" in home
assert "<blockquote" not in home
assert "assets/industrial-push-phase2-discharge.svg" in home
assert "assets/research/01_fractional_oscillator_time.svg" in home
# Preserve all project demonstrations while simplifying their presentation.
projects = html.split("<!-- PAGE 2: PROJECTS -->", 1)[1].split("<!-- PAGE 3: RESEARCH -->", 1)[0]
assert 'class="page academic-projects"' in projects
assert 'id="industrial-project-title"' in projects
assert 'id="empirical-heading"' in projects
assert 'id="projects-thesis-title"' in projects
assert projects.count("data-project-carousel") == 2
assert projects.count('class="project-slide ') == 9, "Missing process stage or numerical plot"
assert projects.count('data-project-go=') == 4
assert projects.count('class="industrial-gallery-figure"') == 5
for marker in ("AI-assisted reconstruction", "No company measurements",
               "Hansen J-test", "four of five industries", "p = 0.311",
               "not a validated trading strategy"):
    assert marker in projects, f"Project evidence or limitation missing: {marker}"
assert "academic-empirical-layout" in editorial_css
# Academic About and Research must keep their distinct content and source notes.
about = html.split("<!-- PAGE 5: ABOUT -->", 1)[1].split("<!-- PAGE 6: CV & CONTACT -->", 1)[0]
assert 'class="page academic-about"' in about
assert 'class="academic-record-list"' in about
assert 'id="about-story-title"' in about
assert 'id="about-education-title"' in about
assert 'id="about-timeline-heading"' in about
assert "Tilburg University" in about and "Utrecht University" in about
assert "<blockquote" not in about
research = html.split("<!-- PAGE 3: RESEARCH -->", 1)[1].split("<!-- PAGE 4: EXPLORING & READING", 1)[0]
assert 'class="page academic-research"' in research
assert 'class="academic-thesis-article thesis-main"' in research
assert research.count('class="thesis-equation"') == 2
assert research.count('class="thesis-figure"') == 3
assert 'class="research-finance-figure"' in research
assert "assets/research/03_caputo_memory_kernel.svg" in research
assert "thesis-source" in research and "Paul Zegeling" in research
assert "not a validated investment strategy" in research
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
assert editorial_css.count("{") == editorial_css.count("}"), "Unbalanced editorial stylesheet"
assert "--layout-max: 1080px" in editorial_css
reading = json.loads((ROOT / "data/reading-list.json").read_text(encoding="utf-8"))
assert reading["papers"] and reading["categories"] and reading["projects"]
assert all(p.get("title") and p.get("url", "").startswith("https://") for p in reading["papers"])

print(f"PASS: {len(site.pages)} pages, {len(site.images)} images, anchors, scientific figures, data and responsive styles.")
print("NOTE: Browser viewport tests, external URLs and CV personal details need manual review.")
