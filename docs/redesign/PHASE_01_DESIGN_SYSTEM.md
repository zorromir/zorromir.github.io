# Phase 1 — Editorial foundations (Figma)

**Status:** Figma foundations and six masthead explorations created; awaiting review before source-code implementation.
**Figma:** https://www.figma.com/design/709SHfK8VVpaZSCeVdpi5S
**Source baseline:** 4eaa07dc65ff648f3e9c93c6146ed8337ba20136
**Working branch:** design/editorial-refinement-v2

## Design intention

Keep the established forest-green/off-white identity but reduce formulaic repeated banners, italic headline fragments, miniature metadata, and decorative cards. Use academic-editorial compositions with genuine research plots and plain language. The designs are studies, not published code.

## Human-authored references

| Reference | Specific idea | Not to copy |
| --- | --- | --- |
| Josef Müller-Brockmann, *Grid Systems in Graphic Design* (1981) | rational alignment with varied compositions | literal posters |
| Edward Tufte, *The Visual Display of Quantitative Information* (1983) | evidence-first charts, unobtrusive decoration | simplified/inaccurate plots |
| Distill, [Communicating with Interactive Articles](https://distill.pub/2020/communicating-with-interactive-articles/) | explanations paired with optional explorable figures | excessive interaction |
| Bartosz Ciechanowski, [technical interactive essays](https://ciechanow.ski/) | animations that explain mechanisms | ornament-only animation |
| W3C, [carousel guidance](https://www.w3.org/WAI/tutorials/carousels/) | keyboard-accessible controls | replacing accessible navigation |

## Foundation variables created in Figma

- 13 base colour primitives, preserving existing CSS: `--ink #20343a`, `--ink-dim #53666a`, `--muted #738488`, `--teal #24766e`, `--line #dbe4e0`, `--bg #f8f9f5`, `--paper #ffffff`, `--soft #edf2ef`, `--warm #b98666`. Additional dark/contrast candidates for exploration only.
- 12 semantic colour aliases covering page/paper/soft/dark surfaces, primary/secondary/muted/accent/inverse text, borders and buttons.
- 12 spacing variables: 4/8/12/16/20/24/32/40/48/64/80/96 px.
- Three radius variables: 0/2/4 px.
- Eight text styles: Editorial display, Section heading, Subsection, UI heading, Main body, Secondary body, Metadata, Action.
- Responsive layout targets: 1440px desktop, 1024px tablet, 390px mobile; the current Figma specimen presents desktop and mobile grid examples, not finished breakpoint-specific site frames.

**Font caveat:** Production CSS specifies Georgia, but Georgia is not available in the connected Figma environment. Figma specimen uses Libre Baskerville as a stand-in; do not silently switch the live website's font.

## Page masthead directions

| Page | Treatment |
| --- | --- |
| Home | Retain one dark hero; factual introduction and strong project access |
| Projects | Light editorial title with project evidence as subsequent visual anchor |
| Research | Pale academic-article masthead, thesis title and subject |
| Exploring & Reading | Small open textual introduction, emphasis on real bibliography |
| About | Quiet personal introduction without inspirational slogan |
| CV & Contact | Direct factual masthead; CV/contact are priority |

The Figma file has page `01 — Foundations` (visual tokens and editorial principles) and page `02 — Page mastheads` (six editable masthead studies).

## Implementation acceptance criteria for Phase 2 and beyond

1. Preserve hash navigation `#home`, `#projects`, `#research`, `#engineering`, `#about`, `#cv`.
2. Preserve actual project source links, correctly labelled synthetic reconstructions and limited research claims.
3. Implement responsive typography with minimum legible body size; avoid 10px explanatory text.
4. Use actual figures at meaningful sizes with captions and axes rather than decorative fake data.
5. Preserve keyboard behavior and reduced-motion semantics.
6. Make one coherent diff on the redesign branch and compare before/after screens before merge.

## Still pending

- Responsive prototype frames for each of the six pages.
- Full component families and variants (button, nav, paper list, figure and carousel).
- Desktop/tablet/mobile browser QA from Phase 0.
- User visual sign-off on the initial design direction.
- No production HTML, CSS or JS has changed as part of Phase 1.
