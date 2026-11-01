# Kelvin Schouten — Portfolio Website

Production source for https://zorromir.github.io/. Static HTML, CSS and JavaScript; GitHub Pages deployment.

## Site structure

- index.html — Home, Projects, Research, Engineering & Making, About, CV & Contact.
- app.js — hash navigation, accessible skip link and mobile menu.
- styles.css — responsive styling.
- assets/cv — publicly accessible English and Dutch CV PDFs.
- CONTENT_GAPS.md — review requirements and Phase 2 project priorities.
- tests/site_check.py — dependency-free structural smoke test.

## Local checks

Run `python -m http.server 8000` then visit http://localhost:8000/. Run `python tests/site_check.py` and `node --check app.js`. Manually review navigation, keyboard focus, mobile screens and PDF links.

## Deployment

Keep main as the existing publishing branch; develop in release branches and merge only after reviewing the PR, sensitive CV details and visual/accessibility checks. The site needs no framework or build step.

## Accuracy

Do not disclose confidential industrial data, unverified 98%/95% metrics or undocumented results. Distinguish academic research, completed coursework and ongoing learning. Engineering interests are not published as completed builds.
