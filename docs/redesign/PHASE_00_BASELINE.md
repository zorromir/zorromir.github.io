# Phase 0 — Existing-site baseline and redesign guardrails

**Captured:** 2026-11-01 · **Status:** Source/CI audit complete; manual cross-viewport browser audit outstanding  
**Production:** https://zorromir.github.io/  
**Repository:** https://github.com/zorromir/zorromir.github.io  
**Frozen baseline commit:** `4eaa07dc65ff648f3e9c93c6146ed8337ba20136`  
**Immutable reference by commit:** https://github.com/zorromir/zorromir.github.io/tree/4eaa07dc65ff648f3e9c93c6146ed8337ba20136  
**Rollback branch:** `backup/pre-editorial-redesign-2026-11-01`  
**Working branch:** `design/editorial-refinement-v2`  
**Deployment branch:** `main` — do not modify directly for this redesign.

This phase freezes the current work. **No production HTML/CSS/JS or content is changed here.** Branching preserves the original website independently of subsequent experiments. The existing site's published layout remains the reference, not the earlier standalone design concept.

## 1. Repository architecture (verified at baseline SHA)

| Path | Role | Change policy |
| --- | --- | --- |
| `index.html` | Six `article.page` screens, shared sections and source links | Edit selected page only, preserve all anchors |
| `styles.css` | Shared tokens, responsive styling and page-specific rules (~113 KB) | Audit cascade before consolidating rules |
| `app.js` | Hash navigation, responsive menu, two project carousels and paper filters (~16 KB) | Preserve keyboard and accessible states |
| `data/reading-list.json` | Six sample research references, five category definitions | Do not invent reading history |
| `assets/research/*.svg` | Three mathematical plots from fractional-oscillator work | Preserve source and interpretation |
| `assets/industrial-*.svg` | Industrial explanatory and model figures | Distinguish synthetic reconstructions from confidential data |
| `assets/empirical-finance-fit.svg` | Historical in-sample academic model comparison | Do not imply out-of-sample profitability |
| `assets/cv/*.pdf` | Public English and Dutch CV PDFs | Verify privacy/version before replacing |
| `projects/industrial-flow/` | Public numerical reproduction scripts and notes | Avoid industrial confidential inputs |
| `projects/empirical-finance/` | Public project documentation | Preserve group-work attribution |
| `tests/site_check.py` | Source structure, links, captions/figures and integrity checks | Extend, do not weaken to make the redesign pass |
| `.github/workflows/site-check.yml` | Source test and JS syntax CI | Require green run before merge |

The tree has 50 entries (40 files and 10 directories) at the frozen baseline.

## 2. Public site page contract

| Route / `data-page` | Current role | Retain | Planned change (later phases) |
| --- | --- | --- | --- |
| `#home` / `home` | Recruitment summary, project features and thesis | Project evidence, CV and GitHub links | One distinctive hero, fewer slogans, stronger real figures |
| `#projects` / `projects` | Industrial modelling and empirical-finance case studies | Technical descriptions, synthetic-data caveats, galleries | Fewer repetitive cards; figures and results first |
| `#research` / `research` | Fractional harmonic oscillator thesis | Equations, plots, thesis source links | Scientific article layout and readable captions |
| `#engineering` / `engineering` | Exploring & Reading | URL hash, paper categories and linked sources | Paper-list style; real status only |
| `#about` / `about` | Academic background and timeline | Accurate biography and dates | Natural writing and simpler editorial layout |
| `#cv` / `cv` | CV, skills and contact | Working PDF downloads and contact links | Compact direct-access design |

The routing hashes `#home`, `#projects`, `#research`, `#engineering`, `#about` and `#cv` are a backwards-compatibility contract. Do not rename `#engineering` without a verified redirect.

## 3. Verified automated baseline

- **Portfolio integrity checks:** SUCCESS on frozen `main` commit. https://github.com/zorromir/zorromir.github.io/actions/runs/41324756628
- **GitHub Pages build and deployment:** SUCCESS on the same frozen commit. https://github.com/zorromir/zorromir.github.io/actions/runs/41324756052
- CI executes `python3 tests/site_check.py` and `node --check app.js` in a GitHub runner. No equivalent independent local execution is claimed in this document.
- The source checker currently tests six page routes, unique IDs, anchors/local assets, alt text, the two project carousels, paper carousel, figure presence, bibliography entries, responsive CSS markers and selected research-integrity text.

**Static audit on baseline:** 6 pages, 14 image elements (all have an `alt` attribute), 11 `figure` elements, 11 `figcaption` elements, 2 project carousel containers, 1 reading carousel, 6 papers. Internal hash links sampled from `href` attributes resolve to element IDs. External targets have *not* been opened one-by-one.

## 4. Research and data-provenance ledger

| Content | Source status | Preserve / verify |
| --- | --- | --- |
| Original six-month industrial modelling research | Employer-era research; original code/data confidential | Do not publish employer measurements, parameters or code |
| Public industrial-flow demonstrations | Independent synthetic/partial reconstruction; some publicly documented AI assistance | Keep the disclosure accurate, concise and separate from visual styling |
| Fractional oscillator thesis | Bachelor's mathematical research; later reproducibility remake | Distinguish original thesis work from rebuilt figures/code |
| Empirical factor models | Historical in-sample MSc group project; separate public implementation | Preserve group attribution and distinguish model fit from trading results |
| Reading library | `library_state: sample_references`, six `reading_status: null` | Do not display example papers as completed reads |
| CV | English and Dutch PDFs published | Verify intended versions and contact details with owner |

**Integrity guardrail:** Improving an AI-like *visual style* must **not** mean falsely denying/erasing AI assistance from public reproduction code, fabricating original research assets, or inventing achievements.

## 5. Design baseline and issues from six supplied full-page screenshots

The user-supplied screenshots provide one desktop-style visual of each page. These screenshots were not produced by a fresh automated viewport capture and may differ from a later deployed commit; treat the frozen commit as source truth.

| Priority | Finding | Impact | Target |
| --- | --- | --- | --- |
| P0 | Repeated deep-green hero structure across almost all pages | Template-like visual rhythm | Distinct introductions, home hero retained |
| P0 | Repetitive italic accent fragments and abstract slogans | Generic, over-styled tone | Specific project and page titles |
| P0 | Many small mono labels and fine-print captions | Weak legibility at ordinary viewing sizes | Accessible type scale |
| P0 | Charts and diagrams often surrounded by large card chrome | Evidence competes with decorative UI | Research visuals as main content |
| P0 | Different types of evidence have different provenance | Risk of misleading captions | Clear original/reproduction/in-sample labels |
| P1 | Repeated card grids and similar section compositions | Pages not sufficiently differentiated | Editorial spreads, open sections, lists |
| P1 | Numerous repeated CSS breakpoint sections (e.g. 17 exact `@media(max-width:620px)` blocks) | Hard-to-maintain cascade | Regression-safe CSS consolidation |
| P1 | Research screenshot appears to include a large blank visual panel | Potential missing illustration or viewport render issue | Reproduce in live browser before changing |
| P1 | Small carousel controls / indicators in screenshots | Harder to discover and operate | Accessible labelled controls |
| P2 | Repeated page-ending tagline and CTA pattern | Mechanical brand repetition | Quieter contact footer |

**Design references for the next phase:** Josef Müller-Brockmann (grid), Edward Tufte (data graphics), Distill (research articles), Bartosz Ciechanowski (purposeful interactives), Nielsen Norman Group (progressive disclosure), W3C WAI (accessible carousels), GOV.UK Design System (legible typography). Each should inform decisions rather than be copied verbatim.

## 6. Baseline capture and remaining verification

**Available:** Six desktop-style screenshots provided by the owner; archived separately in the Phase 0 screenshot ZIP delivered in chat. They are **not** checked into GitHub, and the screenshot ZIP is not the canonical source of code.

**Still required before a full cross-device gate can be claimed:**
- [ ] Fresh browser screenshots at 1440px / 1024px / 390px on *each* page using the frozen commit or matching live build.
- [ ] Verify small-screen menu, keyboard focus/Tab/Escape, click and swipe behaviour of both project carousels, six paper cards and filters.
- [ ] Test previous/next and screen-reader labels; confirm no focus can reach an inert slide.
- [ ] Open all external GitHub/publication URLs and both CV PDFs; check versions and access rights.
- [ ] Investigate whether Research's apparent blank large panel actually renders correctly at all widths.
- [ ] Test 320px narrow viewport and `prefers-reduced-motion`.

See [PHASE_00_QA_MATRIX.md](./PHASE_00_QA_MATRIX.md) for reproducible checklist.

## 7. Exit gate and Phase 1 handoff

**Source and rollback gate: PASSED.** Both branches point to the recorded original main SHA before working-branch documentation commits; code, figures and original links remain untouched on `main`.

**Automated CI baseline gate: PASSED on GitHub's runner.**

**Visual browser gate: OPEN.** Owner-supplied full-page captures are inventoried, but refreshed mobile/tablet and interactive-state checks are not independently complete.

**Next:** Phase 1 — a credited Figma reference board, page-specific editorial wireframes, typographic tokens and a source-grounded content hierarchy. Do not publish visual changes until the browser regression checks and source/provenance review have been completed.
