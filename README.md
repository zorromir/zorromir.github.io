# Quantitative finance and mathematical modelling — portfolio

Source for [zorromir.github.io](https://zorromir.github.io/), a static portfolio presenting research, selected coursework, modelling projects and technical writing.

The site has five views: Home, Projects, Research, Exploring & Reading, and Profile & CV. They are implemented in `index.html`; the `#engineering` URL is retained for Exploring & Reading.

## Structure

| File or directory | Purpose |
| --- | --- |
| `index.html`, `styles.css`, `academic.css` | Page content, layout and responsive styles |
| `app.js` | Navigation, project carousels and bibliography filters |
| `data/reading-list.json` | Research references and their project connections |
| `projects/` | Project scopes, methods and small illustrative simulations |
| `assets/` | Figures, CV PDFs and other website assets |
| `tests/` | Structural and browser checks |

## Running locally

No build framework is required. From the repository root:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/`. The bibliography is loaded from a local JSON file, so the browser should access the site through a local server rather than a `file://` URL.

Basic checks:

```bash
python3 tests/site_check.py
node --check app.js
```

GitHub Actions also checks the site at desktop and mobile viewport sizes.

## Research and data scope

- Pipeline-model illustrations use published equations and hypothetical inputs, not original employer code, measurements or validated industrial results.
- Fractional-oscillator graphics are numerical simulations based on mathematical models, not experimental measurements.
- The empirical-finance results are historical analyses connected to a group study. They do not establish a tradable strategy.

The [industrial modelling repository](https://github.com/zorromir/pipeline-flow-modelling), [fractional-oscillator repository](https://github.com/zorromir/fractional-harmonic-oscillator) and [empirical-finance repository](https://github.com/zorromir/Empirical-Finance) provide the technical context.

GitHub Pages serves the published website from `main`.
