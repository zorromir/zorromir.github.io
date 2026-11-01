# Recruitment readiness — evidence and remaining work

Updated 1 November 2026. The portfolio is intended for quantitative research and modelling internship applications, including research-led asset management and trading firms.

## Evidence a recruiter can inspect now

| Project | Public evidence | Appropriate claim | Limitation |
| --- | --- | --- | --- |
| Industrial pipeline modelling | [Python reconstruction](https://github.com/zorromir/pipeline-flow-modelling), unit tests, numerical figures, mathematical notes | Adapted literature-based models in a six-month industry project; the public demonstration tests numerical assumptions | The public code is AI-assisted, synthetic and partial; no original employer code, parameters, measurements or validated industrial accuracy are public |
| Fractional harmonic oscillator | [Thesis reconstruction](https://github.com/zorromir/fractional-harmonic-oscillator), analytical formulas, numerical examples and tests | BSc mathematics research, with a later reproducibility remake | Public code differs from the original research scripts; computed figures are simulations, not measurements |
| Empirical asset pricing | [Independent public Python analysis](https://github.com/zorromir/Empirical-Finance) and [verified public-data results](https://github.com/zorromir/Empirical-Finance/blob/main/docs/RESULTS_2026-11-01.md) | Completed five-person group study with a separate, independently written public-data implementation; Python 3.10/3.12 tests and live sample integration passed | Original group code and report are not published; subperiod/restriction tests and exhaustive numeric equivalence remain pending |

The website should make these distinctions visible before a recruiter follows a link.

## Priority next steps

1. **Empirical-finance follow-up.** The standalone independent public package is now published, with real-data results, SHA-256 vintage hashes, numerical tests and attribution. Remaining work: reconcile every archived table, add the seasonality subperiod and GMM slope-restriction tests, and consider an out-of-sample robustness exercise before implying any predictive value.
2. **CV privacy check.** The English and Dutch CV PDFs are downloadable from the public website. Review their contact details and confirm both are the intended application versions. Do not automatically remove details without the owner's approval.
3. **Project ownership and claims.** For interviews, prepare a concise explanation of which work was performed in the original industry project versus the public AI-assisted reconstruction, and which empirical-finance work was shared by the group. Avoid unverified numerical performance percentages.
4. **Optional future evidence.** Add out-of-sample financial-model validation only after it has been implemented and independently checked. The present portfolio correctly avoids presenting a live strategy or a validated trading edge.

## Maintenance checks

- All six pages load, and links reach the intended project or CV.
- Home links directly to the public Python/test repositories, and to verified empirical-finance methods.
- Projects identifies the reconstruction boundary and group authorship.
- Thesis and industrial figures are genuine code outputs; synthetic simulations are clearly distinguished from observed data.
- GitHub Actions succeeds and the published mobile view remains readable.

## Scope note

This file is a maintenance checklist, **not a list of unfinished UI screens**. The previous release-gate checklist is superseded; the site and the two standalone research repositories are published. No private coursework or unreleased group materials should be uploaded merely to fill a portfolio gap.
