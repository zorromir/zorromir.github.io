# Empirical asset pricing — verified project summary

**Project:** *An Analysis of Stock Returns Across Industries* (Empirical Finance, Group 03, Tilburg University, September 2026). **Authorship:** five-person academic group. This site attributes all group results to that group; individual contributions are not assigned.

## Research question

Do historical month-of-year returns differ? Do the CAPM and Fama–French five-factor model (FF5) account for five industry portfolios and momentum? Can a CAPM stochastic discount factor (SDF) price the selected industry assets?

The empirical distinction matters: **better explanatory fit need not imply smaller pricing errors.**

## Data and estimation

Five U.S. value-weighted portfolios from the [Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html): **Oil, Banks, Textiles, Toys and Retail**.

| Analysis | Period | Observations | Statistical method |
|---|---|---:|---|
| Calendar-month effects | Jan. 1927–Dec. 2025 | 1,188 | Month dummies; 11-restriction Wald tests; HAC(24); Holm across five industries |
| CAPM and FF5 comparisons | Jul. 1963–Jun. 2026 | 756 | Matched-sample OLS coefficient estimates with HAC(24) inference |
| SDF | Jul. 1963–Jun. 2026 | 756 | Two-step GMM, six moment conditions and two parameters; NW six-lag weighting |

**Source reconciliation:** The archived CAPM CSV has an extra July 2026 observation. Independent verification explicitly truncates both factor-model datasets to the published June 2026 endpoint.

## Verified results

**Calendar effects.** All five full-sample industry-level Wald tests reject equality of monthly means after Holm adjustment with HAC(24); the largest full-sample R² is **2.14%**. Only **Textiles** remains significant in all three equal-length subperiods. The Oil rejection is sensitive to some shorter HAC bandwidths.

**Model fit versus pricing.** FF5 has higher adjusted R² than CAPM for all five industries. With HAC(24) inference, the negative FF5 alphas of Banks, Textiles and Toys are individually significant at 5%. After correcting the **five FF5 industry alpha tests** using Holm, **Textiles** (adjusted p ≈ **0.0076**) and **Toys** (adjusted p ≈ **0.0362**) remain significant; Banks does not (adjusted p ≈ **0.1231**). No CAPM industry alpha is individually significant.

**Momentum.** Sample intercepts are approximately **+0.714% monthly** (CAPM) and **+0.753% monthly** (FF5) with HAC(24) p-values below 0.0001. These are in-sample model intercepts, not a realized investable strategy return.

**SDF model check.** The original two-step GMM procedure was independently reproduced: estimated slope **c ≈ 3.571**, Hansen J ≈ **4.777** (p ≈ **0.311**) and slope-restriction p ≈ **0.456**. Centering moment autocovariances in a sensitivity check gives p_J ≈ 0.287. Both calculations fail to reject; neither validates the model.

### Critical interpretation

- **Calendar predictability does not alone imply market inefficiency**: returns can vary with conditional risk premia (Fama, 1991).
- **Non-rejection does not mean model confirmation**, especially where test portfolios have closely related factor exposures.
- **The SDF test did not include momentum portfolios** among its six moment conditions.
- **Improved adjusted R² and alpha tests answer different questions.**
- These are historical in-sample observations, without transaction-cost and out-of-sample validation.
- The original report's factor-model t-statistics were based on conventional OLS inference despite text referring to HAC. The corrected HAC calculations above were performed as an independent audit.

## Independent robustness and out-of-sample checks

A later [public Python diagnostic](https://github.com/zorromir/Empirical-Finance/blob/main/docs/ROBUSTNESS_RESULTS_2026-11-01.md) tests the sensitivity of the previously reported results. Across three equally sized calendar subsamples, only Textiles rejects the month-of-year equality null in all three. Across tested FF5 HAC bandwidths (6, 12, 24, 36), Textiles and Toys retain significant alphas after Holm adjustment. None of the alternative SDF covariance specifications rejects the J test at 5%.

A separately defined **lagged-factor expanding-window forecast**, using previous-month predictors rather than contemporaneous factors, performs worse than an expanding historical-mean benchmark for Oil, Banks, Toys and Retail; Textiles' OOS R² improvement is only about **0.52%**. This does not establish an investable edge. Inputs are not historical point-in-time vintages, and no execution costs or trading simulation are included.

## Implementation status

**Numerical review:** Calendar tests reproduce the original paper. Matched-sample CAPM and FF5 coefficient estimates reproduce the report. Independent HAC p-values and Holm corrections have been calculated. The original GMM algorithm reproduces its reported values.

**Independent public implementation:** A new [Empirical-Finance Python repository](https://github.com/zorromir/Empirical-Finance) downloads public Kenneth French data, runs calendar Wald tests, matched-sample CAPM/FF5 regressions, momentum intercepts and two-step GMM, and saves source ZIP hashes. [The public-data results from 1 November 2026](https://github.com/zorromir/Empirical-Finance/blob/main/docs/RESULTS_2026-11-01.md) are numerically close to the archived central findings. This is newly written research code, **not** the original five-person group archive. Subperiod analysis and the extra SDF slope-restriction test are not yet implemented. Exact numerical identity across all original tables has not been established.

Do not upload the original five-person report or its cover page with student IDs publicly without agreement of co-authors. This repository summarizes group findings with attribution rather than claiming that the complete group project is solo work.

**Relevant references:** [Fama (1991), efficient markets and the joint-hypothesis problem](https://doi.org/10.1111/j.1540-6261.1991.tb04636.x); Gibbons, Ross and Shanken (1989), joint alpha testing; Kenneth French Data Library.
