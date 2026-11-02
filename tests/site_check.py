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
expected = ["home", "projects", "research", "engineering", "about"]
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
assert "how reliable backtests are" in home
assert "Fama–French factor extensions" in home
assert "value, residual momentum and low-volatility signals" in home
assert '<a href="#engineering">Exploring &amp; Reading</a>' in home
assert "<blockquote" not in home
assert "assets/industrial-push-phase2-discharge.svg" in home
assert "assets/research/01_fractional_oscillator_time.svg" in home
# Preserve all project demonstrations while simplifying their presentation.
projects = html.split("<!-- PAGE 2: PROJECTS -->", 1)[1].split("<!-- PAGE 3: RESEARCH -->", 1)[0]
assert 'class="page academic-projects"' in projects
assert 'id="industrial-project-title"' in projects
assert 'id="empirical-heading"' in projects
assert 'id="projects-thesis-title"' not in projects
assert 'class="shell academic-project-thesis"' not in projects
assert projects.count("data-project-carousel") == 2
assert projects.count('class="project-slide ') == 9, "Missing process stage or numerical plot"
assert projects.count('data-project-go=') == 4
# Phase 4: the two existing carousels link to their matching examples.
assert projects.count('data-project-carousel=') == 2
assert 'id="industrial-model-stages"' in projects
assert 'id="industrial-numerical-figures"' in projects
assert projects.count('class="industrial-stage-figure-links"') == 4
assert projects.count('class="industrial-gallery-stage-links"') == 5
assert projects.count('data-project-jump="figures"') == 6
assert projects.count('data-project-jump="stages"') == 6
for target in ("stages", "figures"):
    assert f'data-project-carousel="{target}"' in projects
for link_target in ("industrial-model-stages", "industrial-numerical-figures"):
    assert f'href="#{link_target}"' in projects
assert 'const projectCarouselControllers = new Map()' in js
assert "document.querySelectorAll('a[data-project-jump]')" in js
assert 'controller.show(index)' in js
assert 'controller.carousel.focus({ preventScroll: true })' in js
assert 'prefers-reduced-motion: reduce' in js
assert 'Phase 4 — model-to-figure navigation' in editorial_css
# Phase 5: mobile fixes follow the live narrow-screen interaction audit.
assert "Phase 5 — narrow-screen fixes from live QA" in editorial_css
assert "industrial-gallery .project-gallery-dots button" in editorial_css
assert "grid-template-columns: repeat(4, minmax(0, 1fr))" in editorial_css
assert 'academic.css?v=industrial-link-spacing-20261102' in html
assert projects.count('Python-generated illustration · synthetic inputs · Select plot to enlarge') == 5
assert 'Published relationships · public Python reconstructions · illustrative assumptions' in projects
assert 'independently coded examples' not in projects
assert 'academic.css?v=industrial-links-20261102' in html
assert 'app.js?v=industrial-links-20261102' in html
# All four industrial stages use semantic, browser-native mathematical notation.
assert projects.count('class="industrial-stage-equation"') == 4
assert projects.count('xmlns="http://www.w3.org/1998/Math/MathML"') == 4
assert projects.count("<mfrac>") == 5
assert projects.count("<msup>") == 1
assert projects.count("<msub>") >= 5
assert 'industrial-stage-equation">dx' not in projects
assert 'industrial-stage-equation math' in editorial_css
assert 'Phase 3 — industrial carousel layout refinement' in editorial_css
assert 'academic.css?v=industrial-layout-20261102' in html
assert 'grid-template-columns: minmax(0, .96fr) minmax(0, 1.04fr)' in editorial_css
assert 'grid-template-columns: minmax(0, 1.1fr) minmax(0, .9fr)' in editorial_css
assert projects.count('class="industrial-gallery-figure"') == 5
for marker in ("without company measurements", "Hansen J-test",
               "four of five industries", "p = 0.311",
               "not a validated trading strategy"):
    assert marker in projects, f"Project evidence or limitation missing: {marker}"
assert "academic-empirical-layout" in editorial_css
assert 'industrial-literature-title' in projects
assert 'SCOPE &amp; REPRODUCIBILITY' not in projects
reference_rule = editorial_css.split("#projects .academic-industrial-project .industrial-reference-strip {", 1)[1].split("}", 1)[0]
assert "border: 0;" in reference_rule and "border-top:" not in reference_rule
assert 'Numerical verification is not experimental validation.' not in projects
assert '>View code and technical documentation ↗</a>' in projects
# The gallery keeps five full-size figures but no per-slide Python source links.
industrial_figures = projects.split('<section id="industrial-numerical-figures"', 1)[1].split('<section class="industrial-project-conclusion"', 1)[0]
assert industrial_figures.count('Expand figure ↗') == 5
assert 'View Python source' not in industrial_figures
assert 'blob/main/examples/' not in industrial_figures
assert projects.count('class="industrial-project-conclusion"') == 1
assert projects.index('class="industrial-project-conclusion"') < projects.index('id="industrial-literature-title"')
assert 'id="industrial-project-conclusion-title"' in projects
assert 'The links open the publishers' + chr(39) + ' pages.' not in projects
assert '.industrial-project-conclusion h3' in editorial_css
assert 'Fluivac — Push, Blow, Rinse &amp; Dry' in projects
assert 'Public Python reconstruction and tests' not in projects
assert 'industrial-process-photos' in projects
assert projects.count('class="industrial-photos-grid"') == 1
assert projects.count('src="https://fluivac.com/wp-content/uploads/2021/10/') == 4
assert 'industrial-photos-grid' in editorial_css
for caption in ("Push", "Blow", "Rinse", "Dry"):
    assert projects.count(f"<figcaption>{caption}</figcaption>") == 1, f"Missing photo stage: {caption}"
assert "industrial-photos-credit" not in projects
assert "Use the arrows or select a stage" not in projects
assert "The process follows four stages." in projects
assert "border-bottom: 0;" in editorial_css.split("#home .academic-home-intro {", 1)[1].split("}", 1)[0]
intro_rule = editorial_css.split("#home .academic-home-intro::after {", 1)[1].split("}", 1)[0]
assert "left: 0;" in intro_rule and "right: 0;" in intro_rule
assert "border-bottom: 1px solid var(--line);" in intro_rule
assert "#home .academic-home-record > div:last-child { margin-bottom: 0; border-bottom: 0; }" in editorial_css
assert "#home .academic-home-intro::after { bottom: 27px; }" in editorial_css
assert 'Four stages of product recovery and the mathematical ideas used to describe them.' in projects
assert projects.count('class="industrial-literature-citation"') == 5
assert projects.count('href="https://doi.org/10.1115/1.4031508"') == 1
assert projects.count('href="https://doi.org/10.1038/s41597-024-03441-7"') == 1
assert 'Tijsseling et al. (2016) ↗' not in projects
assert 'Chen et al. (2024) ↗' not in projects
assert 'industrial-literature-list' in editorial_css
for doi in ("https://doi.org/10.1016/0301-9322(89)90023-2", "https://doi.org/10.1016/j.ijmultiphaseflow.2012.03.003", "https://doi.org/10.1016/j.ijmultiphaseflow.2012.12.003"):
    assert doi in projects, f"Missing journal link: {doi}"
# Academic About and Research must keep their distinct content and source notes.
about = html.split("<!-- PAGE 5: PROFILE & CV", 1)[1].split("  </main>", 1)[0]
assert 'class="page academic-about academic-profile"' in about
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
assert 'href="assets/research/The_Fractional_Harmonic_Oscillator__Analysis_and_Computations.pdf"' in research, "Thesis must link directly to the published PDF"
assert 'type="application/pdf">Thesis (PDF)</a>' in research
assert "data-thesis-pdf-path" not in html and "method: 'HEAD'" not in js
assert "not a validated investment strategy" in research
# Profile & CV is one page, with the old #cv URL still supported by JS.
assert 'class="page academic-about academic-profile"' in about
assert 'id="cv" class="legacy-route-anchor"' in about
assert 'data-page="cv"' not in html and 'data-nav="cv"' not in html
assert 'data-nav="about">Profile &amp; CV</a>' in html
assert "hash === 'cv' ? 'about'" in js
for section_id in ("about-title", "about-story-title", "about-education-title",
                   "about-timeline-heading", "about-interests-title", "about-methods-title",
                   "about-languages-title", "about-contact-title"):
    assert f'id="{section_id}"' in about, f"Missing merged profile section: {section_id}"
assert about.count("<h1") == 1
assert about.count("id=\"about-education-title\"") == 1
assert "The Hague University of Applied Sciences" in about
assert "Tilburg University" in about and "Utrecht University" in about
assert "Panel Data Econometrics" in about
assert "Monte Carlo" in about and "Mathematics and Physics Tutor" in about
assert "Dutch (native)" in about and "English (proficient)" in about
assert "mailto:schoutenkelvin@gmail.com" in about
assert "academic-profile-skills" in editorial_css
assert "footer-cv-link" in editorial_css
# The shared footer appears outside individual articles, so this single PDF
# link is available from every routed page, beside GitHub and Email.
footer = html.split('<footer class="site-footer">', 1)[1]
assert footer.count('class="footer-cv-link"') == 1
assert footer.count('href="assets/cv/Kelvin_Schouten_CV_EN.pdf?v=20261101-newcv"') == 1
assert 'type="application/pdf"' in footer
assert 'target="_blank"' in footer
assert 'mailto:schoutenkelvin@gmail.com' in footer
assert 'https://github.com/zorromir' in footer
assert html.count("assets/cv/Kelvin_Schouten_CV_EN.pdf?v=20261101-newcv") == 2
assert "https://github.com/zorromir/pipeline-flow-modelling" in html
assert "https://github.com/zorromir/fractional-harmonic-oscillator" in html
assert "projects/empirical-finance/README.md" in html
assert "https://github.com/zorromir/Empirical-Finance" in html
assert "ROBUSTNESS_RESULTS_2026-11-01.md" in html
assert "four of five industries" in html
assert "independent public python reconstruction" in html.lower()
assert "Python-generated illustration · synthetic inputs" in html
assert "ILLUSTRATIVE DATA — NOT EMPIRICAL RESULTS" not in html
kernel = (ROOT / "assets/research/03_caputo_memory_kernel.svg").read_text(encoding="utf-8")
assert "<svg" in kernel and kernel.count("<path") >= 3, "Memory-kernel figure absent"
assert html.count("data-project-carousel") == 2
# Reading is a bibliography, not a one-paper-at-a-time carousel.
reading_page = html.split("<!-- PAGE 4: EXPLORING & READING", 1)[1].split("<!-- PAGE 5: PROFILE & CV", 1)[0]
assert 'class="page academic-exploring"' in reading_page
assert 'class="academic-coursework-heading"' in reading_page
assert reading_page.count('class="shell academic-exploring-section academic-projects-section"') == 1
assert reading_page.count('class="shell academic-exploring-section academic-coursework-section"') == 1
assert reading_page.index('id="now-projects-title"') < reading_page.index('id="coursework-title"')
assert 'Research &amp; continuing work' in reading_page
assert 'Tilburg University · MSc Quantitative Finance' in reading_page
current_project_section = reading_page.split('<h2 id="now-projects-title">', 1)[1].split('id="coursework-title"', 1)[0]
assert current_project_section.count('class="academic-project-entry"') == 3
assert "Empirical asset pricing" in current_project_section
assert "Fama–French factor extensions" in current_project_section
assert "Machine learning for asset pricing" in current_project_section
assert "Fractional harmonic oscillator" not in current_project_section
assert "Two-phase flow modelling" not in current_project_section
assert "Asset pricing · Quantitative research" in current_project_section
assert "Machine Learning · Asset pricing" in current_project_section
assert current_project_section.count(">Project</a>") == 2
assert ">Related papers</a>" not in current_project_section
assert ">Project scope</a>" not in current_project_section
for path in ("projects/current-research/fama-french-factor-extensions.md", "projects/current-research/machine-learning-asset-pricing.md"):
    content = (ROOT / path).read_text(encoding="utf-8")
    assert "## Research question" in content and "## Project scope" in content
    assert "### Main research references" in content
    assert path in current_project_section
ml_scope = (ROOT / "projects/current-research/machine-learning-asset-pricing.md").read_text(encoding="utf-8")
ml_stages = ml_scope.split("### Planned stages", 1)[1].split("### Main research references", 1)[0]
assert len([line for line in ml_stages.splitlines() if line.lstrip().split(".", 1)[0].isdigit() and line.lstrip().startswith(tuple(f"{n}." for n in range(1, 12)))]) == 11
for reference in ("Empirical Asset Pricing via Machine Learning", "Machine Learning Goes Global", "The Probability of Backtest Overfitting", "The Deflated Sharpe Ratio"):
    assert reference in ml_scope
assert "chronological training, validation and test samples" in ml_scope

factor_scope = (ROOT / "projects/current-research/fama-french-factor-extensions.md").read_text(encoding="utf-8")
assert "### Planned stages" in factor_scope
assert len([line for line in factor_scope.split("### Planned stages", 1)[1].split("### Main research references", 1)[0].splitlines() if line[:2] in ("1.", "2.", "3.", "4.", "5.", "6.", "7.")]) == 7
for reference in ("A Five-Factor Asset Pricing Model", "Resurrecting the Value Premium", "Residual Momentum", "The Volatility Effect", "Settling the Size Matter"):
    assert reference in factor_scope
assert reading_page.count('class="academic-current-projects academic-coursework-projects"') == 1
for title in ("Panel-data estimation and dynamic models", "Stochastic interest rates and derivative pricing", "Supplier decisions under uncertainty", "Hedging and pricing hybrid insurance claims"):
    assert title in reading_page, f"Missing course project: {title}"
assert "not completed results" in reading_page
assert '<h2 id="now-projects-title">My projects</h2>' in reading_page
assert '<h2 id="coursework-title" class="academic-coursework-heading">MSc coursework</h2>' in reading_page
assert '<h2 id="learning-title">Courses I\'m taking</h2>' in reading_page
course_list = reading_page.split('<ul class="academic-learning-list academic-courses-list"', 1)[1].split('</ul>', 1)[0]
for course in ("Panel Data", "Empirical Finance", "Risk &amp; Regulation", "Valuation &amp; Risk", "Decision Making Under Uncertainty"):
    assert f"<li>{course}</li>" in course_list
assert course_list.count("<li>") == 5
assert "data-paper-collection-note" not in reading_page
assert "data-paper-collection-note" not in js
assert "These are additional references connected to my projects" not in html
assert 'id="explore-suppliers"' in reading_page
assert 'id="explore-backtesting"' in reading_page
assert reading_page.index('id="explore-backtesting"') < reading_page.index('id="now-projects-title"')
assert reading_page.count('class="academic-focus-paper"') == 4
assert "How reliable is a backtest?" in reading_page
focus_section = reading_page.split('id="exploring-now-title"', 1)[1].split('id="now-projects-title"', 1)[0]
assert "Related empirical-finance work" not in focus_section
assert "Course project scope" not in focus_section
assert 'class="academic-focus-related"' not in focus_section
assert "https://doi.org/10.1007/s00291-026-00869-8" in reading_page
for marker in ("data-paper-library", "data-paper-filters", "data-paper-list",
               "data-paper-fallback", "data-paper-count", "Other papers &amp; references",
               "not a record of completed reading", "Courses I'm taking"):
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
assert "--layout-max: 960px" in editorial_css
reading = json.loads((ROOT / "data/reading-list.json").read_text(encoding="utf-8"))
assert reading["papers"] and reading["categories"] and reading["projects"]
assert all(p.get("title") and p.get("url", "").startswith("https://") for p in reading["papers"])
# Current readings appear in topic groups; only other references are repeated in the fallback shelf.
current_papers = [p for p in reading["papers"] if p["reading_status"] == "reading"]
reference_papers = [p for p in reading["papers"] if p["reading_status"] != "reading"]
assert len(current_papers) == 4
assert len(reference_papers) == reading_page.count("class=\"paper-citation\"")
for paper in reading["papers"]:
    assert paper["title"].replace("&", "&amp;") in reading_page
    assert paper["url"] in reading_page
for paper in current_papers:
    assert f'href="{paper["url"]}"' in reading_page
assert all(p["reading_status"] == "reading" for p in current_papers)
assert "sample_references" == reading["library_state"]
assert reading["papers"][0]["id"] == "merzifonluoglu-et-al-2026-supplier-risk"
assert {p["id"] for p in current_papers} == {"merzifonluoglu-et-al-2026-supplier-risk", "bailey-lopez-de-prado-2014", "white-2000-reality-check", "bailey-borwein-prado-zhu-pbo"}
assert reading["papers"][0]["reading_status"] == "reading"
assert "optimization" in reading["papers"][0]["category_ids"]
assert any(p["id"] == "supplier-optimization" for p in reading["projects"])
assert len({p["id"] for p in reading["papers"]}) == len(reading["papers"])

print(f"PASS: {len(site.pages)} pages, {len(site.images)} images, anchors, scientific figures, data and responsive styles.")
print("NOTE: Browser viewport tests, external URLs and CV personal details need manual review.")
