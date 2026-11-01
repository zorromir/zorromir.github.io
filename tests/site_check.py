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
# Header is text-only and homepage no longer repeats the site navigation.
assert 'class="brand-symbol"' not in html
assert 'class="brand-label"' in html
assert 'class="academic-home-links"' not in home
assert 'class="academic-home-record"' in home
assert "padding-top: clamp(56px, 6.2vw, 72px)" in editorial_css
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
# All four industrial stages use semantic, browser-native mathematical notation.
assert projects.count('class="industrial-stage-equation"') == 4
assert projects.count('xmlns="http://www.w3.org/1998/Math/MathML"') == 4
assert projects.count("<mfrac>") == 3
assert projects.count("<msup>") == 1
assert projects.count("<msub>") >= 9
assert 'industrial-stage-equation">dx' not in projects
assert 'industrial-stage-equation math' in editorial_css
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
# CV & Contact: confirm the actual PDF and contacts, without dashboard cards.
cv = html.split("<!-- PAGE 6: CV & CONTACT -->", 1)[1].split("  </main>", 1)[0]
assert 'class="page academic-cv"' in cv
for section_id in ("cv-title", "cv-overview-title", "cv-education-title",
                   "cv-experience-title", "cv-skills-title", "cv-contact-title"):
    assert f'id="{section_id}"' in cv, f"Missing CV section: {section_id}"
assert cv.count("assets/cv/Kelvin_Schouten_CV_EN.pdf?v=20261101-newcv") == 2
assert 'download="Kelvin_Schouten_CV.pdf"' in cv
assert "mailto:schoutenkelvin@gmail.com" in cv
assert "https://github.com/zorromir" in cv
assert "The Hague University of Applied Sciences" in cv
assert "Tilburg University" in cv and "Utrecht University" in cv
assert "Monte Carlo" in cv and "Panel Data Econometrics" in cv
for legacy_class in ("cv-paper", "cv-sidebar", "cv-download-panel",
                     "cv-areas-panel", "cv-contact-band"):
    assert f'class="{legacy_class}"' not in cv
assert "Phase 7 — CV & Contact." in editorial_css
assert "https://github.com/zorromir/pipeline-flow-modelling" in html
assert "https://github.com/zorromir/fractional-harmonic-oscillator" in html
assert "projects/empirical-finance/README.md" in html
assert "https://github.com/zorromir/Empirical-Finance" in html
assert "ROBUSTNESS_RESULTS_2026-11-01.md" in html
assert "four of five industries" in html
assert "independent public python reconstruction" in html.lower()
assert "AI-assisted reconstruction" in html
assert "do not establish predictive accuracy against company measurements" in html
assert "ILLUSTRATIVE DATA — NOT EMPIRICAL RESULTS" not in html
kernel = (ROOT / "assets/research/03_caputo_memory_kernel.svg").read_text(encoding="utf-8")
assert "<svg" in kernel and kernel.count("<path") >= 3, "Memory-kernel figure absent"
assert html.count("data-project-carousel") == 2
# Reading is a bibliography, not a one-paper-at-a-time carousel.
reading_page = html.split("<!-- PAGE 4: EXPLORING & READING", 1)[1].split("<!-- PAGE 5: ABOUT -->", 1)[0]
assert 'class="page academic-exploring"' in reading_page
for marker in ("data-paper-library", "data-paper-filters", "data-paper-list",
               "data-paper-fallback", "data-paper-count", "Most recent readings",
               "Reading progress has not been confirmed", "Currently studying",
               "not establish predictive accuracy against company measurements"):
    assert marker in reading_page, f"Reading-page content missing: {marker}"
assert "data-paper-carousel" not in html
assert "coverFor(" not in js and "makeSlide(" not in js
assert "academic-paper-filter" in js and "academic-paper-detail" in js
assert "academic-literature-list" in editorial_css
assert "aria-current" in js and "aria-expanded" in js and "inert" in js
assert "fetch('data/reading-list.json')" in js
assert "prefers-reduced-motion" in css and "--layout-gutter" in css
assert css.count("{") == css.count("}"), "Unbalanced stylesheet blocks"
assert editorial_css.count("{") == editorial_css.count("}"), "Unbalanced editorial stylesheet"
assert "--layout-max: 1080px" in editorial_css
reading = json.loads((ROOT / "data/reading-list.json").read_text(encoding="utf-8"))
assert reading["papers"] and reading["categories"] and reading["projects"]
assert all(p.get("title") and p.get("url", "").startswith("https://") for p in reading["papers"])
# Verify that the no-JavaScript bibliography matches the JSON source list.
assert len(reading["papers"]) == reading_page.count("class=\"paper-citation\"")
for paper in reading["papers"]:
    assert paper["title"].replace("&", "&amp;") in reading_page
    assert paper["url"] in reading_page
assert "sample_references" == reading["library_state"]

print(f"PASS: {len(site.pages)} pages, {len(site.images)} images, anchors, scientific figures, data and responsive styles.")
print("NOTE: Browser viewport tests, external URLs and CV personal details need manual review.")
