#!/usr/bin/env python3
"""Browser smoke checks for the academic portfolio, including screenshots.

Run: python3 tests/browser_check.py
Requires Playwright and its Chromium browser.
"""
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.request import urlopen
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PAPERS = sum(p["reading_status"] != "reading" for p in json.loads((ROOT / "data/reading-list.json").read_text(encoding="utf-8"))["papers"])
SHOTS = ROOT / "artifacts" / "qa"
SHOTS.mkdir(parents=True, exist_ok=True)
ROUTES = ("home", "projects", "research", "engineering", "about")
VIEWPORTS = (("desktop", 1440, 900), ("tablet", 810, 1080),
             ("mobile", 390, 844), ("narrow-mobile", 320, 720))


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format_string, *args):
        pass


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def check_site(browser, base, device, width, height):
    page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
    exceptions = []
    page.on("pageerror", lambda error: exceptions.append(str(error)))

    for route in ROUTES:
        page.goto(f"{base}/index.html#{route}", wait_until="load", timeout=30000)
        page.locator("#" + route).wait_for(state="visible")
        check(page.locator(f'[data-page="{route}"] h1:visible').count() == 1,
              f"{device}/{route}: missing or duplicate visible page heading")
        check(page.locator('h1:visible').count() == 1,
              f"{device}/{route}: multiple visible h1 elements")
        pdf = page.locator(".site-footer .footer-cv-link")
        check(pdf.count() == 1
              and pdf.get_attribute("href").startswith("assets/cv/Kelvin_Schouten_CV_EN.pdf"),
              f"{device}/{route}: footer PDF link missing")
        check(page.locator('[data-nav][aria-current="page"]').count() == 1,
              f"{device}/{route}: navigation did not update")
        check(page.locator(f'[data-nav="{route}"][aria-current="page"]').count() == 1,
              f"{device}/{route}: wrong active navigation link")
        size = page.evaluate("""() => ({
            client: document.documentElement.clientWidth,
            scroll: document.documentElement.scrollWidth
        })""")
        check(size["scroll"] <= size["client"] + 2,
              f"{device}/{route}: horizontal overflow {size}")
        # Every route uses the same outer grid as the navigation and footer.
        # Keep the research figures and project carousels free to use the grid.
        alignment = page.evaluate("""route => {
            const box = element => {
                const rect = element.getBoundingClientRect();
                return {left: rect.left, width: rect.width};
            };
            const header = box(document.querySelector('.site-header .shell'));
            const footer = box(document.querySelector('.site-footer .shell'));
            const title = box(document.querySelector('#' + route + ' h1'));
            const sections = [...document.querySelectorAll('#' + route + ' > .shell')]
                .map(box);
            return {header, footer, title, sections};
        }""", route)
        check(len(alignment["sections"]) >= 2,
              f"{device}/{route}: page sections missing: {alignment}")
        for name, rect in [("footer", alignment["footer"]),
                           ("title", alignment["title"]),
                           *[(f"section {i}", item)
                             for i, item in enumerate(alignment["sections"], start=1)]]:
            check(abs(rect["left"] - alignment["header"]["left"]) < 1.5,
                  f"{device}/{route}: {name} left edge shifts: {alignment}")
            if name != "title":
                check(abs(rect["width"] - alignment["header"]["width"]) < 1.5,
                      f"{device}/{route}: {name} width shifts: {alignment}")
        if device in ("desktop", "mobile"):
            page.screenshot(path=str(SHOTS / f"{device}-{route}.png"), full_page=True,
                            animations="disabled", timeout=60000)
        check(not exceptions, f"{device}/{route}: JS exception: {exceptions}")

    # Existing external links to #cv must open the new combined profile.
    page.goto(f"{base}/index.html#cv", wait_until="load")
    page.locator("#about").wait_for(state="visible", timeout=5000)
    check(page.locator('#about h1').inner_text() == "Profile & CV",
          f"{device}: legacy CV link did not open Profile & CV")
    check(page.locator('[data-nav="about"][aria-current="page"]').count() == 1,
          f"{device}: legacy CV link did not select Profile & CV navigation")

    page.goto(f"{base}/index.html#home", wait_until="load")
    check(page.locator(".brand img").count() == 0,
          f"{device}: header monogram still visible")
    check(page.locator("#home .academic-home-links").count() == 0,
          f"{device}: repeated homepage quick links remain")
    if width > 810:
        vertical = page.evaluate("""() => {
          const title = document.querySelector('#home-title').getBoundingClientRect();
          const label = document.querySelector('#home .academic-home-record span').getBoundingClientRect();
          return {midpoint: title.top + title.height / 2, labelTop: label.top};
        }""")
        check(vertical["labelTop"] >= vertical["midpoint"] - 8,
              f"{device}: current studies not lowered toward name midpoint: {vertical}")
    # Drive keyboard focus to the skip link explicitly after repeated route navigations.
    # The browser can retain an earlier focus target across page.goto calls.
    page.keyboard.press("Tab")
    page.locator(".skip").focus()
    check(page.evaluate("document.activeElement.classList.contains('skip')"),
          f"{device}: skip link cannot receive focus")
    check(page.evaluate("""() => {
        const style = getComputedStyle(document.activeElement);
        return style.outlineStyle !== 'none' && style.outlineWidth !== '0px';
    }"""), f"{device}: keyboard focus indicator missing")

    if width <= 620:
        # The mobile menu needs to open, navigate and close.
        toggle = page.locator("#menu-toggle")
        check(toggle.is_visible(), f"{device}: mobile menu toggle absent")
        toggle.click()
        check(toggle.get_attribute("aria-expanded") == "true",
              f"{device}: menu did not expand")
        page.locator('[data-nav="research"]').click()
        # Hashchange dispatch is asynchronous after the menu link click.
        page.locator("#research").wait_for(state="visible", timeout=5000)
        check(toggle.get_attribute("aria-expanded") == "false",
              f"{device}: menu did not close after navigation")

    page.goto(f"{base}/index.html#projects", wait_until="load")
    carousels = page.locator('[data-project-carousel]')
    check(carousels.count() == 2, f"{device}: missing project carousels")
    equations = page.locator("#projects .industrial-stage-equation math")
    check(equations.count() == 4, f"{device}: expected four rendered MathML equations")
    for i in range(equations.count()):
        equation = equations.nth(i)
        metrics = equation.evaluate("""math => ({
            namespace: math.namespaceURI,
            height: math.getBoundingClientRect().height,
            width: math.getBoundingClientRect().width
        })""")
        check(metrics["namespace"] == "http://www.w3.org/1998/Math/MathML"
              and metrics["height"] >= 12 and metrics["width"] > 0,
              f"{device}: equation {i+1} failed to render: {metrics}")
        check(equation.locator(":scope > mrow").count() == 1,
              f"{device}: equation {i+1} has no grouped mathematical row")
    if width > 810:
        size = equations.first.evaluate("""math => ({
          equation: math.getBoundingClientRect().width,
          container: math.closest('.industrial-stage-equation').clientWidth,
          fraction: math.querySelector('mfrac').getBoundingClientRect().width
        })""")
        check(size["equation"] < size["container"] * .85
              and size["fraction"] < size["container"] * .65,
              f"{device}: fraction stretches across the panel: {size}")
    for i in range(2):
        carousel = carousels.nth(i)
        check(carousel.locator('[data-project-count]').inner_text().startswith("01"),
              f"{device}: first slide not selected")
        carousel.locator('[data-project-next]').click()
        check(carousel.locator('[data-project-count]').inner_text().startswith("02"),
              f"{device}: next arrow did not work")

    page.goto(f"{base}/index.html#engineering", wait_until="load")
    page.locator('[data-paper-list]:not([hidden])').wait_for(timeout=12000)
    check(page.locator('[data-paper-list] > li').count() == EXPECTED_PAPERS,
          f"{device}: expected {EXPECTED_PAPERS} bibliography entries")
    check("Large Sample Properties" in page.locator('[data-paper-list] > li').first.inner_text(),
          f"{device}: reference shelf did not load")
    check(page.locator('#explore-backtesting .academic-focus-paper').count() == 3,
          f"{device}: missing backtesting reading links")
    check(page.locator('#explore-suppliers .academic-focus-paper').count() == 1,
          f"{device}: missing supplier reading link")
    check(page.locator('#explore-backtesting').bounding_box()["y"] < page.locator('#now-projects-title').bounding_box()["y"],
          f"{device}: exploration topics should appear before projects")
    check(page.locator('#engineering .academic-projects-section').count() == 1
          and page.locator('#engineering .academic-coursework-section').count() == 1,
          f"{device}: project/coursework sections missing")
    project_section = page.locator('#engineering .academic-projects-section')
    course_section = page.locator('#engineering .academic-coursework-section')
    check(project_section.bounding_box()["y"] < course_section.bounding_box()["y"],
          f"{device}: coursework does not start after projects")
    check(course_section.get_by_role("heading", name="MSc coursework").count() == 1,
          f"{device}: distinct MSc coursework heading missing")
    check(page.locator('#engineering .academic-courses-list > li').count() == 5,
          f"{device}: expected five listed MSc courses")
    current_projects = page.locator('#engineering .academic-current-projects').first
    check(current_projects.locator('.academic-project-entry').count() == 3,
          f"{device}: unexpected number of current project cards")
    check(current_projects.get_by_text('Fama–French factor extensions').count() == 1
          and current_projects.get_by_text('Machine learning for asset pricing').count() == 1,
          f"{device}: new current projects missing")
    check(current_projects.get_by_text('Fractional harmonic oscillator').count() == 0
          and current_projects.get_by_text('Two-phase flow modelling').count() == 0,
          f"{device}: previous projects still in current projects")
    page.locator('[data-paper-filters] button', has_text="Econometrics").click()
    check(page.locator('[data-paper-list] > li').count() >= 2,
          f"{device}: bibliography filter did not work")
    check(not exceptions, f"{device}: JS exception: {exceptions}")
    page.close()


def check_without_javascript(browser, base):
    # With JavaScript disabled, all five sections must remain reachable and
    # the hand-written reference shelf must match the unpublished-reading subset.
    context = browser.new_context(java_script_enabled=False,
                                  viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.goto(base + "/index.html#engineering", wait_until="load")
    for route in ROUTES:
        check(page.locator("#" + route).is_visible(),
              "No-JS page hidden: " + route)
    check(page.locator("[data-paper-fallback] li").count() == EXPECTED_PAPERS,
          "No-JS bibliography missing")
    check(page.locator("#cv").count() == 1,
          "No-JS legacy #cv anchor missing")
    check(page.locator("#main-nav").is_visible(),
          "No-JS navigation unavailable")
    page.close()
    context.close()


def main():
    handler = partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with urlopen(base + "/assets/cv/Kelvin_Schouten_CV_EN.pdf", timeout=15) as response:
            check(response.status == 200, "English CV PDF unavailable")
            check(response.read(4) == b"%PDF", "CV download is not a PDF")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
            try:
                for device, width, height in VIEWPORTS:
                    check_site(browser, base, device, width, height)
                    print(f"PASS: {device}, {width}px — routes, keyboard and interactions")
                check_without_javascript(browser, base)
                print(f"PASS: no-JavaScript document and {EXPECTED_PAPERS}-entry bibliography")
            finally:
                browser.close()
    finally:
        server.shutdown()
    print("PASS: browser QA, 10 screenshots and fallback in artifacts/qa")


if __name__ == "__main__":
    main()
