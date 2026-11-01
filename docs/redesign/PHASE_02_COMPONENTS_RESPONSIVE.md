# Phase 2 — Shared components and responsive direction

**Date:** 2026-11-01
**Status:** Component library created in Figma; responsive browser proof-of-concept supplied as a standalone HTML file in ChatGPT; production implementation not started.
**Figma file:** https://www.figma.com/design/709SHfK8VVpaZSCeVdpi5S
**Working branch:** `design/editorial-refinement-v2`
**Published branch:** `main` (unchanged)

## Goal

Make the portfolio feel like a personal mathematical research publication, not a generic AI-generated agency template. Reuse a small number of reliable components but vary the composition between pages. Preserve existing page routes, project evidence, and scientific provenance.

## Completed editable Figma components

The `03 — Components & responsive` Figma page contains:

| Native Figma object | Variants | Intended code correspondence | Design reason |
| --- | --- | --- | --- |
| `KS / Action button` | filled, outline, quiet | `.button`, `.button-primary`, `.button-outline`, `.text-link` | Restrained, consistent action treatment |
| `KS / Site header` | desktop, mobile | `.site-header`, `.main-nav`, `.menu-toggle` | Preserve the working sticky header and accessible menu |
| `KS / Project summary` | master component | `.feature`, `.industrial-summary` and section content | Explain genuine methods and evidence; avoid excessive card chrome |
| `KS / Research figure` | master component | `figure`, `figcaption`, research figure classes | Use real computed plots with captions and precise provenance |
| `KS / Paper entry` | master component | paper list/carousel rows driven by `data/reading-list.json` | Use accurate bibliography metadata, not decorative books |
| `KS / Carousel controls` | master component | `[data-project-prev]`, `[data-project-next]`, `[data-project-count]` | Visible, readable controls to navigate real comparisons |

These are editable native shapes and text. They are **design specimens**, not functional browser controls. The research figure uses an explicit asset slot rather than invented data.

The `02 — Page mastheads` Figma page was created during Phase 1 but its masthead frames were not preserved in a subsequent read; do not consider that gallery validated.

**Figma tool constraint:** Figma Starter caps this file at three pages, and further Figma calls hit the plan's MCP-call limit during Phase 2. Additional responsive Figma frames remain pending; do not claim they are completed.

## Responsive implementation specification

| Width | Layout | Navigation | Figure treatment |
| --- | --- | --- | --- |
| Desktop — 1440px | Up to 1200px editorial container, 12-column conceptual grid, generous negative space | Horizontal six-link nav | Full-size figure with visible units/caption |
| Tablet — 1024px | 2-column compositions where feasible; reduce horizontal padding | Compact horizontal nav until overflow, then mobile menu | Figures may occupy entire width |
| Mobile — 390px | Single reading column, 18px side gutters, body copy ≥15px | Explicit Menu button with aria-expanded and Escape close | Stacked figures without horizontal overflow |
| Narrow — 320px | Same single column and touch-sized controls | Menu only | Labels and equations must wrap or scroll intentionally |

Do not force every page into the same two-column dark hero. The Home page retains one dark masthead; Research uses an academic-article introduction; Projects, Reading, About and CV use light editorial introductions.

## Design and accessibility contract

1. Body copy 15–17px minimum; avoid tiny 10px paragraphs. Metadata may use 11px only for secondary labels.
2. Serif headlines + sans-serif explanatory text; production CSS uses Georgia and Inter. Figma uses Libre Baskerville as a serif stand-in only.
3. No decorative numbers, dots or labels without meaning. Do not repeat italic-accent headline formulas.
4. Research figures must be the verified code-generated `assets/` sources, with axis labels and clear original/reproduction/in-sample distinction.
5. Preserve real technical wording, project attribution, reconstruction and AI-assistance disclosures, and reading-status uncertainty.
6. Keep `#engineering` URL intact despite the visible name “Exploring & Reading”.
7. Controls must work for keyboard users; support focus-visible and reduced motion. Do not mark prototypes as accessibility-tested before browser QA.
8. Keep working navigation and carousels in `app.js`; CSS refactoring must not remove scripts or source-integrity checks.

## Page-level layout decisions

| Page | Shared components | Page-specific composition |
| --- | --- | --- |
| Home | header, action links, featured project | one distinctive dark intro, then actual research figures |
| Projects | project summaries, figure, carousel controls | large plotted evidence and method walkthrough |
| Research | article headings, figure and captions | narrow reading measure, wide technical figure |
| Exploring & Reading | paper rows and source links | openly presented bibliography, with honest sample-data disclaimer |
| About | header, typography, restrained dividers | narrative text and academic timeline, not repeated card grid |
| CV & Contact | action buttons, factual sections | direct CV PDF links and professional contact info |

## Human-authored reference mapping

- **Josef Müller-Brockmann,** `Grid Systems in Graphic Design`: underlying alignment; allow asymmetric compositions.
- **Edward Tufte,** `The Visual Display of Quantitative Information`: research figures get visual precedence over decoration.
- **Distill**, `Communicating with Interactive Articles`: optional exploration next to rigorous explanation.
- **W3C WAI**, carousel tutorials: accessible controls and navigation behavior.
- **GOV.UK Design System**, typography: readable text and clear navigational states.

## Code implementation handoff (Phase 3)

Before production CSS changes:
- Inspect `styles.css` for duplicate rules and produce a cascade audit; consolidate safely instead of appending more overrides.
- Scope new styles under meaningful section/component classes and keep existing `app.js` behavior.
- Compare screenshots across desktop 1440, tablet 1024, mobile 390 and narrow 320.
- Re-run GitHub Actions `python3 tests/site_check.py` and `node --check app.js`.
- Verify both CV PDFs and project/publication links manually.
- Review results on a PR, then merge to `main` only after approving the design.

### Phase 2 completion status
- [x] Reusable native Figma specimens and editable text
- [x] Button appearance variants and desktop/mobile header variants
- [x] Research figure, project summary, paper entry, carousel control structures
- [x] Responsive breakpoint specification
- [x] Source-to-Figma component mapping
- [x] Standalone HTML responsive design study (delivered in conversation, not committed)
- [ ] Responsive frames for six pages directly in Figma (Starter limit)
- [ ] Visual viewport/browser regression validation (browser access limited in this session)
- [ ] Acceptance/sign-off for production rollout
