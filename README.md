# Kelvin Schouten — Portfolio website

A clean, responsive one-page portfolio website for quantitative finance, mathematical modelling and research. Built using plain HTML/CSS/JavaScript; **no build step, framework, backend or paid hosting required**.

## Start locally

1. Unzip the folder.
2. Open `index.html` in a browser, or open the folder in VS Code and use the **Live Server** extension.
3. The live GitHub section fetches public repositories from the GitHub API. If you're offline or over the API rate limit, a link to the GitHub profile is shown instead.

## Publish with GitHub Pages

1. On GitHub, sign in as **zorromir** and create a **public** repository named `zorromir.github.io` (or use an existing one).
2. Upload **all contents of this folder** to the root of the `main` branch. The `index.html` file should be in the root, not inside another folder.
3. Open **Settings → Pages → Build and deployment → Source → Deploy from a branch**.
4. Choose **main** and **/(root)**, then click **Save**.
5. The site will be available at **https://zorromir.github.io/** after deployment. This URL is only an expected address, **not an already-deployed site**.

You can also use **GitHub Desktop** to publish changes: clone your site repository, copy the files into it, commit and push. For future edits, modify files in VS Code, then commit/push; Pages will redeploy.

Official guide: https://docs.github.com/en/pages/quickstart

## Edit content

| File | What to change |
|---|---|
| `index.html` | Biography, education, projects, skills, work experience, page titles and contact email |
| `styles.css` | Colours, typography, spacing, mobile layouts |
| `script.js` | `GITHUB_USERNAME`, maximum number of repo cards, theme and navigation behaviour |
| `assets/cv/*.pdf` | Replace with new CVs using the same filenames |
| `assets/favicon.svg` | The KS-style website icon |

The website intentionally uses **only public GitHub repositories**. Nonpublic repositories are never accessed by visitors or listed on the page. Its selected-work section includes an industrial modelling project described from your CV and an Empirical Finance coursework project. It does not publish project code or results without your review.

## Before sharing with recruiters

- [ ] Check spelling of your name, institutions and degree titles.
- [ ] Confirm the project description is approved for public disclosure by the commissioning company. Do not include confidential model parameters, charts or client information.
- [ ] Verify that publishing your **CV PDF** is acceptable: it contains your phone number and email address. Remove or replace those details before publishing if you want to keep them private.
- [ ] Check technical methods listed under Skills and in each project against tools you actually used.
- [ ] Add links to your best public **project repositories** once the code is ready; use README files, figures and methodology for each.
- [ ] Proofread every page and test the PDF download buttons after publishing.

## Possible version 2

- Add a case-study page for the industrial modelling project, using non-confidential diagrams and verified results.
- Add a dedicated empirical-finance project page with charts, methodology and reproducible code.
- Connect a custom domain through GitHub Pages settings (optional).

© Kelvin Schouten. Created as an editable personal website template.
