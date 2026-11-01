# Phase 3 — Homepage editorial implementation

**Status:** Implemented on the redesign branch; draft PR / browser visual review required before publishing.
**Branch:** `design/editorial-refinement-v2`
**Figma direction:** https://www.figma.com/design/709SHfK8VVpaZSCeVdpi5S

## What changed

- Reconciled the redesign branch with the latest `main` commit before touching the homepage. No recent project evidence links, documentation, or test changes were discarded.
- Replaced the repeated italic-slogan homepage H1 with **Mathematical modelling & quantitative finance**.
- Introduced factual educational context without overclaiming or inventing results.
- Changed subsequent headings to **Selected projects**, **Mathematics of memory**, and **Reading & ongoing work**.
- Removed the second formulaic concluding research slogan.
- Preserved the two real project figures (industrial synthetic reproduction and academic empirical finance) with their current provenance labels.
- Promoted primary projects, original numerical figures, Github links, thesis and CV through typography/spacing rather than decorative components.
- Added `home-editorial.css` as a narrowly scoped stylesheet, included immediately after `styles.css`. Deliberately avoided appending more scattered overrides to the existing ~113 KB of CSS.
- Kept `app.js`, shared nav, hash routes, and other five page bodies unchanged.
- Extended `tests/site_check.py` with Phase 3 checks for heading structure, research caveats, responsive rules and preserved source links.

## Source changes

| File | Change |
| --- | --- |
| `index.html` | Only homepage headings, introduction, limited content and the new stylesheet reference |
| `home-editorial.css` | Dedicated desktop, tablet and mobile homepage layout plus reduced motion |
| `tests/site_check.py` | Additional source-level regression checks |

## Editorial design decisions and credited references

- **Josef Müller-Brockmann:** a reliable underlying grid and sparse headings; not a copy of any particular poster.
- **Edward Tufte:** evidence-first figure sizing and captions; no invented synthetic graph styled as research.
- **Distill:** clear explanatory writing paired with authentic figures and links to methods.
- **W3C/WAI:** preserve keyboard navigation and responsive readability.

The goal is less generic promotional copy and fewer identical card structures, **not** to conceal genuine AI assistance in published code reconstructions. Scientific disclosure remains intact.

## Merge gate

- [ ] GitHub Actions `python3 tests/site_check.py` green
- [ ] GitHub Actions `node --check app.js` green
- [ ] Visual comparison at 1440 / 1024 / 390 / 320 pixels
- [ ] No horizontal overflow or broken text wrapping
- [ ] Mobile menu and hash navigation still work
- [ ] All three public project code links and EN/NL CV remain accessible
- [ ] Caption/source/provenance status readable
- [ ] Review draft pull request; do not merge without user approval

**Known limitation:** GitHub Pages publishes `main` only. The branch version is not yet the live website, and a complete visual screenshot gate is not claimed.
