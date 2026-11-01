# Phase 0 — Baseline regression matrix

**Baseline commit:** `4eaa07dc65ff648f3e9c93c6146ed8337ba20136`  
**Source audit:** [PHASE_00_BASELINE.md](./PHASE_00_BASELINE.md)  
**Legend:** `PASS (CI)` verified by GitHub Actions; `PENDING (browser)` not yet independently verified. Do not tick browser items from a screenshot alone.

## A. Automated checks

- [x] PASS (CI) — `python3 tests/site_check.py` on the baseline commit
- [x] PASS (CI) — `node --check app.js` on the baseline commit
- [x] PASS (CI) — published Pages deployment job completed successfully
- [x] PASS (source audit) — six unique `data-page` sections retained in expected order
- [x] PASS (source audit) — internal hash targets sampled from links exist
- [x] PASS (source audit) — all 14 `img` elements include `alt`
- [x] PASS (source audit) — `reading-list.json` has six sample papers and unconfirmed statuses

## B. Navigational smoke tests for each viewport

Viewport matrix: `1440×900` desktop / `1024×768` tablet / `390×844` mobile / optional `320×700` narrow.

| Area | Desktop | Tablet | Mobile | Checks |
| --- | --- | --- | --- | --- |
| Home `#home` | ☐ | ☐ | ☐ | Intro, project links, CV and Github visible; no overflow |
| Projects `#projects` | ☐ | ☐ | ☐ | Both case studies and source labels |
| Research `#research` | ☐ | ☐ | ☐ | Equations, 3 plots, no empty figure panel |
| Reading `#engineering` | ☐ | ☐ | ☐ | Category filters, paper sources, sample notice |
| About `#about` | ☐ | ☐ | ☐ | Biography, timeline, links |
| CV `#cv` | ☐ | ☐ | ☐ | CV panel, EN/NL PDF links, contact |
| Shared header | ☐ | ☐ | ☐ | Menu, active state, Escape, outside-click |
| Shared footer | ☐ | ☐ | ☐ | Contact links and readable footer |
| Project carousel 1 | ☐ | ☐ | ☐ | Push/Blow/Rinse/Dry stages, buttons, keyboard |
| Project carousel 2 | ☐ | ☐ | ☐ | Previous/next and figure captions |
| Paper carousel | ☐ | ☐ | ☐ | Six papers, category filters and keyboard |
| Accessibility | ☐ | ☐ | ☐ | Tab order, visible focus, contrast, labels |
| Reduced motion | ☐ | ☐ | ☐ | System preference respected |

Record screenshot filenames and any differences here before CSS modifications.

## C. External and download checks

- [ ] Verify `https://github.com/zorromir/pipeline-flow-modelling`
- [ ] Verify `https://github.com/zorromir/fractional-harmonic-oscillator`
- [ ] Verify `https://github.com/zorromir/Empirical-Finance`
- [ ] Verify `projects/empirical-finance/README.md` link
- [ ] Open English CV PDF from live website; verify correct version, contact details and copy/privacy
- [ ] Open Dutch CV PDF if the site links it; verify correct version
- [ ] Open each of the six paper publication URLs; ensure correct target
- [ ] Verify the original `#engineering` route continues to work

## D. Scientific content and provenance

- [ ] Confirm source/label for every industrial figure; no employer confidential data
- [ ] Check synthetic/illustrative notes are legible and unambiguous
- [ ] Confirm empirical finance figure indicates historical in-sample results and group context
- [ ] Confirm fractional-oscillator axes, mathematical notation, captions and original-versus-reproduction distinction
- [ ] Confirm the paper library retains unconfirmed reading status until owner provides actual reading history
- [ ] Confirm the original public reconstruction assistance disclosure remains accurate
- [ ] Check the CV skills and project claims against published repository evidence

## E. Exit checks before merging a redesigned page

- [ ] No page route renamed; all six hashes still resolve
- [ ] Source checker and `node --check` green on pull request
- [ ] Desktop/tablet/mobile screenshot comparisons completed
- [ ] Charts, equations and captions checked by a human reviewer
- [ ] WCAG keyboard behaviour, focus and reduced motion verified
- [ ] Change diff contains no sensitive code, private employer data or fabricated performance metrics
- [ ] Merged only after the site owner reviews and approves the visual diff

**Status as of 2026-11-01:** A complete; B–E pending manual checks. No changes to public `main`.
