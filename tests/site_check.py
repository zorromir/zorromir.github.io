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
cv_theme = (ROOT / "cv-theme.css").read_text(encoding="utf-8")

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
# Refined CV / motivation-letter design spans all five routed pages.
assert 'cv-theme.css?v=projects-research-story-20261115' in html
assert 'family=Lato' in html
assert 'class="brand-mark"' in html
assert 'class="site-contact"' in html
assert html.count('class="cv-page-eyebrow"') == 4
assert "Academic record / Background" in html
assert "Selected research / Mathematics &amp; quantitative finance" in html
assert "Mathematics / Numerical methods" in html
assert "Ongoing questions / Literature" in html
assert "#193347" in cv_theme and "#a18c68" in cv_theme
assert "var(--cv-rule)" in cv_theme
assert "math { font-family:inherit" not in cv_theme

assert 'class="academic-home-links"' not in home
assert 'class="academic-home-record"' in home
assert "padding-top: clamp(56px, 6.2vw, 72px)" in editorial_css
assert "The Fractional Harmonic Oscillator" in home
assert "how reliable backtests are" in home
assert home.count('class="academic-work-year"') == 3
assert "Fama–French factor extensions" in home
assert "value, residual momentum and low-volatility signals" in home
assert '<a href="#engineering">Exploring &amp; Reading</a>' in home
assert "<blockquote" not in home
assert "assets/industrial-push-phase2-discharge.svg" in home
assert "assets/research/01_fractional_oscillator_time.svg" in home
# Preserve clear project summaries and working links to the public reports.
projects = html.split("<!-- PAGE 2: PROJECTS -->", 1)[1].split("<!-- PAGE 3: RESEARCH -->", 1)[0]
assert 'class="page academic-projects"' in projects
assert 'id="industrial-project-title"' in projects and 'id="empirical-heading"' in projects
assert count_class("project-paper-entry") == 2
assert projects.count('class="project-paper-questions"') == 2
assert projects.count('<h3>What I investigated</h3>') == 2
assert projects.count('class="project-paper-copy"') == 2
assert projects.count('class="project-paper-credentials"') == 2
assert "Six months · Two days a week" in projects
assert "I spent six months on this project, working on it two days a week." in projects
assert "stages Push, Blow, Rinse and Dry instead" in projects
assert "project-paper-note" not in projects
assert "The amount of liquid in the pipe changes" in projects
assert "A large part of the work was not just solving equations" in projects
assert "What I learned most from this project" in projects
assert projects.count('<aside class="project-paper-questions"') == 2
for panel in re.findall(r'<aside class="project-paper-questions"[^>]*>(.*?)</aside>', projects, re.S):
    assert panel.count("<li>") == 3
assert '<details' not in projects and 'data-project-carousel' not in projects
assert '<details' not in projects and 'data-project-carousel' not in projects
assert "I started from a practical question" in projects
assert "if an asset-pricing model explains more variation in returns" in projects
assert "The original paper is a five-person group study" not in projects
assert "The linked report is a redacted" not in projects
assert "not validated industrial predictions" not in projects
assert 'assets/reports/fluivac-public-technical-excerpt.pdf' in projects
for filename in ("fluivac-public-technical-excerpt.pdf", "Empirical_finance.pdf"):
    report_bytes = (ROOT / "assets" / "reports" / filename).read_bytes()
    assert report_bytes.startswith(b"%PDF-") and len(report_bytes) > 50_000, (
        f"Missing, invalid or unexpectedly short public report: {filename}"
    )
assert 'assets/reports/Empirical_finance.pdf' in projects
assert 'https://github.com/zorromir/pipeline-flow-modelling' not in projects
assert 'https://github.com/zorromir/Empirical-Finance' in projects
assert "Open CV" not in projects
assert "'industrial-model-stages': 'industrial-project-title'" in js
assert "'empirical-heading': 'empirical-heading'" in js
assert 'data-project-next' not in js
assert '#projects .project-paper-layout' in cv_theme
assert '#projects .project-paper-questions' in cv_theme
assert 'app.js?v=projects-paper-first-20261115' in html
assert 'cv-theme.css?v=projects-research-story-20261115' in html

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
assert research.count('class="thesis-figure"') == 2
assert research.count('class="thesis-figure thesis-figure-feature"') == 1
assert research.count('<details class="research-technical-details">') == 1
assert research.count('<summary>') == 1
assert research.index('class="research-thesis-overview"') < research.index('class="research-visual-summary"') < research.index('<details class="research-technical-details">')
assert '<aside class="research-thesis-questions"' in research
assert research.count('What I investigated</h3>') == 1
assert 'aria-label="Open full-size fractional oscillator displacement figure"' in research
assert 'research-finance-overview' in research
assert 'href="#empirical-heading"' in research
assert "Research overview — recruiter-first" in cv_theme
assert "grid-template-columns:minmax(0,1fr) minmax(260px,360px)" in cv_theme
assert "research-technical-details[open]" in cv_theme
assert "max-width:690px" in cv_theme
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
assert "document.title = name === 'engineering'" in js
assert "? 'Exploring & Reading'" in js
assert 'app.js?v=projects-paper-first-20261115' in html
for section_id in ("about-title", "about-story-title", "about-education-title",
                   "about-timeline-heading", "about-learning-title", "about-other-interests-title", "about-methods-title",
                   "about-languages-title", "about-contact-title"):
    assert f'id="{section_id}"' in about, f"Missing merged profile section: {section_id}"
assert about.count("<h1") == 1
assert about.count('id="about-other-interests-title"') == 1
assert about.index('id="about-learning-title"') < about.index('id="about-other-interests-title"') < about.index('id="about-methods-title"')
assert 'id="about-interests-title"' not in about
assert 'when one question naturally leads to another' in about
assert 'learning through conversation works particularly well for me' in about
assert 'almost like a Socratic discussion partner' in about
assert 'more like following my own curiosity' in about
assert "Background, education, experience and my approach to learning." in about
assert 'chess, 3D printing, reading, climbing, strategy games and meditation.' in about
assert 'class="academic-profile-pdf" aria-label="Curriculum vitae document"' in about
assert html.count("Kelvin_Schouten_CV_EN.pdf?v=20261115-replacement") == 2
assert "Kelvin_Schouten_CV_EN.pdf?v=20261101-newcv" not in html
cv_bytes = (ROOT / "assets/cv/Kelvin_Schouten_CV_EN.pdf").read_bytes()
assert cv_bytes.startswith(b"%PDF-") and len(cv_bytes) > 50_000

assert 'class="shell academic-page-intro academic-profile-intro"' in about
assert 'class="academic-profile-intro-copy"' in about
assert 'class="academic-profile-pdf-label">Curriculum vitae <small>PDF · English</small>' in about
assert 'Open CV <span aria-hidden="true">↗</span>' in about
assert 'View CV (PDF)' not in about
assert '#about .academic-profile-pdf-label' in editorial_css
profile_cv_rule = editorial_css.split('#about .academic-profile-pdf {', 1)[1].split('}', 1)[0]
assert 'max-width: 380px;' in profile_cv_rule
assert 'academic.css?v=profile-cv-alignment-20261102' in html
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
assert footer.count('href="assets/cv/Kelvin_Schouten_CV_EN.pdf?v=20261115-replacement"') == 1
assert 'type="application/pdf"' in footer
assert 'target="_blank"' in footer
assert 'mailto:schoutenkelvin@gmail.com' in footer
assert 'https://github.com/zorromir' in footer
assert html.count("assets/cv/Kelvin_Schouten_CV_EN.pdf?v=20261115-replacement") == 2
assert "https://github.com/zorromir/pipeline-flow-modelling" in html
assert "https://github.com/zorromir/fractional-harmonic-oscillator" in html
assert "https://github.com/zorromir/Empirical-Finance" in html
assert "https://github.com/zorromir/Empirical-Finance" in html
assert "ROBUSTNESS_RESULTS_2026-11-01.md" in html
assert "After the group project, I built a separate public Python version" in html
assert "After the group project, I built a separate public Python version" in html
assert "Public Python examples" not in projects
assert "ILLUSTRATIVE DATA — NOT EMPIRICAL RESULTS" not in html
kernel = (ROOT / "assets/research/03_caputo_memory_kernel.svg").read_text(encoding="utf-8")
assert "<svg" in kernel and kernel.count("<path") >= 3, "Memory-kernel figure absent"
assert html.count("data-project-carousel") == 0
# Research questions and project descriptions now carry their own linked sources.
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
assert "Asset pricing · Factor research" in current_project_section
assert "Machine learning · Asset pricing" in current_project_section
assert current_project_section.count(">Research plan</a>") == 2
learning_panels = re.findall(r'<aside class="academic-project-learning"[^>]*>(.*?)</aside>', current_project_section, re.S)
assert len(learning_panels) == 3
assert all(panel.count("<li>") == 3 for panel in learning_panels)
assert current_project_section.count('<h4>What I want to understand</h4>') == 3
assert "Research project narratives + learning-question sidebars" in cv_theme
assert "grid-template-columns:minmax(0, 1fr) minmax(215px, .45fr)" in cv_theme
assert "@media(max-width:820px)" in cv_theme
for url in ("https://ssrn.com/abstract=3705218",
            "https://doi.org/10.1016/j.jempfin.2011.01.003",
            "https://ssrn.com/abstract=980865",
            "https://ssrn.com/abstract=3686583",
            "https://doi.org/10.1093/rfs/hhaa009",
            "https://doi.org/10.1016/j.jedc.2023.104725",
            "https://doi.org/10.1057/s41260-021-00237-x",
            "https://doi.org/10.21314/JCF.2016.322",
            "https://doi.org/10.3905/jpm.2014.40.5.094"):
    assert f'href="{url}"' in current_project_section, f"Missing project source: {url}"

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
assert reading_page.index('id="explore-backtesting"') < reading_page.index('id="explore-suppliers"')
assert reading_page.count('class="academic-focus-topic"') == 2
focus_section = reading_page.split('id="exploring-now-title"', 1)[1].split('id="now-projects-title"', 1)[0]
focus_learning_panels = re.findall(r'<aside class="academic-project-learning"[^>]*>(.*?)</aside>', focus_section, re.S)
assert len(focus_learning_panels) == 2
assert all(panel.count("<li>") == 3 for panel in focus_learning_panels)
assert focus_section.count('<h4>What I want to understand</h4>') == 2
assert "How much apparent performance comes from testing many strategies?" in focus_section
assert "How do risk preferences and CVaR change supplier rankings?" in focus_section
assert "Learning goals beside the two Exploring questions" in cv_theme
assert "#engineering .academic-focus-section .academic-project-learning" in cv_theme
assert reading_page.count('class="academic-project-learning"') == 5

assert 'class="academic-focus-reading"' not in reading_page
assert 'class="academic-focus-paper"' not in reading_page
assert "How reliable is a backtest?" in reading_page
focus_section = reading_page.split('id="exploring-now-title"', 1)[1].split('id="now-projects-title"', 1)[0]
assert "Related empirical-finance work" not in focus_section
assert "Course project scope" not in focus_section
assert 'class="academic-focus-related"' not in focus_section
assert "https://doi.org/10.1007/s00291-026-00869-8" in reading_page
for marker in ("data-paper-library", "data-paper-filters", "data-paper-list",
               "data-paper-fallback", "data-paper-count", "Other papers &amp; references",
               "Reading for this question", "Selected research papers"):
    assert marker not in reading_page, f"Unused paper list still visible: {marker}"
for source in ("White (2000)", "Bailey et al. (2014)",
               "Bailey and López de Prado (2014)", "Merzifonluoglu et al. (2026)",
               "Arellano and Bond (1991)", "Fama and French (2015)"):
    assert source in reading_page, f"Missing inline research source: {source}"
assert "Courses I'm taking" in reading_page
assert "data-paper-carousel" not in html
assert "coverFor(" not in js and "makeSlide(" not in js
assert "academic-paper-filter" not in js and "academic-paper-detail" not in js
assert "data-paper-library" not in js and "fetch('data/reading-list.json')" not in js
assert "aria-current" in js and "aria-expanded" in js
assert "pages.forEach(page => { page.hidden = page.dataset.page !== name; });" in js
assert "Integrated literature references" in cv_theme
assert "prefers-reduced-motion" in css and "--layout-gutter" in css
assert css.count("{") == css.count("}"), "Unbalanced stylesheet blocks"
assert editorial_css.count("{") == editorial_css.count("}"), "Unbalanced editorial stylesheet"
assert "--layout-max: 960px" in editorial_css
reading = json.loads((ROOT / "data/reading-list.json").read_text(encoding="utf-8"))
assert reading["papers"] and reading["categories"] and reading["projects"]
assert all(p.get("title") and p.get("url", "").startswith("https://") for p in reading["papers"])
# Keep the JSON catalogue as a source of record, but show papers contextually.
current_papers = [p for p in reading["papers"] if p["reading_status"] == "reading"]
reference_papers = [p for p in reading["papers"] if p["reading_status"] != "reading"]
assert len(current_papers) == 4 and len(reference_papers) == 5
# Only actively discussed papers need a direct inline link; the remaining
# literature records stay in the JSON catalogue and supporting PDFs.
for paper in current_papers:
    assert f'href="{paper["url"]}"' in reading_page, f"Reading reference not linked: {paper['id']}"
assert all(p["url"] in reading_page for p in current_papers)
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
