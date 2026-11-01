#!/usr/bin/env python3
"""Browser smoke checks for the academic portfolio, including screenshots.

Run: python3 tests/browser_check.py
Requires Playwright and its Chromium browser.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.request import urlopen
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "artifacts" / "qa"
SHOTS.mkdir(parents=True, exist_ok=True)
ROUTES = ("home", "projects", "research", "engineering", "about", "cv")
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
        if device in ("desktop", "mobile"):
            page.screenshot(path=str(SHOTS / f"{device}-{route}.png"), full_page=True,
                            animations="disabled", timeout=60000)
        check(not exceptions, f"{device}/{route}: JS exception: {exceptions}")

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
    for i in range(2):
        carousel = carousels.nth(i)
        check(carousel.locator('[data-project-count]').inner_text().startswith("01"),
              f"{device}: first slide not selected")
        carousel.locator('[data-project-next]').click()
        check(carousel.locator('[data-project-count]').inner_text().startswith("02"),
              f"{device}: next arrow did not work")

    page.goto(f"{base}/index.html#engineering", wait_until="load")
    page.locator('[data-paper-list]:not([hidden])').wait_for(timeout=12000)
    check(page.locator('[data-paper-list] > li').count() == 6,
          f"{device}: expected six bibliography entries")
    page.locator('[data-paper-filters] button', has_text="Econometrics").click()
    check(page.locator('[data-paper-list] > li').count() >= 2,
          f"{device}: bibliography filter did not work")
    check(not exceptions, f"{device}: JS exception: {exceptions}")
    page.close()


def check_without_javascript(browser, base):
    # With JavaScript disabled, all six sections must remain reachable and
    # the hand-written bibliography must still list all six citations.
    context = browser.new_context(java_script_enabled=False,
                                  viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.goto(base + "/index.html#engineering", wait_until="load")
    for route in ROUTES:
        check(page.locator("#" + route).is_visible(),
              "No-JS page hidden: " + route)
    check(page.locator("[data-paper-fallback] li").count() == 6,
          "No-JS bibliography missing")
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
                print("PASS: no-JavaScript document and six-entry bibliography")
            finally:
                browser.close()
    finally:
        server.shutdown()
    print("PASS: browser QA, 12 screenshots and fallback in artifacts/qa")


if __name__ == "__main__":
    main()
