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
VIEWPORTS = (("desktop", 1440, 900), ("tablet", 810, 1080), ("mobile", 390, 844))


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
                    print(f"PASS: {device}, {width}px — six routes and interactions")
            finally:
                browser.close()
    finally:
        server.shutdown()
    print("PASS: browser checks and twelve screenshots in artifacts/qa")


if __name__ == "__main__":
    main()
