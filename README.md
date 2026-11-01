# Kelvin Schouten — Portfolio website

Source for [zorromir.github.io](https://zorromir.github.io/), a static portfolio about mathematical modelling, academic research and quantitative finance.

## Pages and structure

The six sections are Home, Projects, Research, Exploring & Reading, About, and CV & Contact. These are views in `index.html`; the original `#engineering` URL for Exploring & Reading is kept so existing links continue working.

| Path | Purpose |
| --- | --- |
| `index.html` | All six pages, project descriptions, figures and links |
| `styles.css` | Shared editorial design, page styles and responsive rules |
| `app.js` | Navigation, mobile menu, project carousels and paper filters |
| `data/reading-list.json` | Publication bibliography and project connections |
| `assets/research/` | Computed fractional-oscillator figures |
| `assets/industrial-*.svg` | Independent synthetic pipeline-model reproductions |
| `assets/empirical-finance-fit.svg` | Historical, in-sample MSc group analysis figure |
| `assets/cv/` | Publicly downloadable CV PDFs |
| `tests/site_check.py` | Dependency-free structural checks |

## Work locally

Start a local web server because the reading carousel loads JSON:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/`. No framework or build step is required.

Check the repository before publishing:

```sh
python3 tests/site_check.py
node --check app.js
```

GitHub Actions runs both checks on pull requests and pushes to `main`. Also review the actual layout, carousel buttons, keyboard interaction and PDF downloads in a browser before major releases.

## Research integrity

Industrial graphics are **synthetic, non-confidential reproductions**, not measurements from the company or its original code. Fractional-oscillator figures are computed mathematical model outputs, not empirical observations. The finance plot compares historical, in-sample regression results from a group study, not the performance of an investment strategy.

Do not include confidential industrial inputs or unverified performance claims. The CV files are public: check personal details in the PDFs before sharing.

## Deployment

GitHub Pages publishes the root of `main`. Prefer feature branches and review changes before merging.
