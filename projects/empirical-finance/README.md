# Empirical asset pricing — research project summary

**Status:** Completed group report (five co-authors), Tilburg University, September 2026. Individual responsibilities have not been assigned in the public summary.

**Source:** *An analysis of stock returns across industries*, Empirical Finance (35M1C9-M-6), group 03.

## Question

Can calendar effects predict U.S. industry portfolio returns? Do the CAPM and Fama–French five-factor model account for mean returns and momentum? Does a classic CAPM stochastic discount factor satisfy its pricing restrictions on these test assets?

## Data and empirical design

Five U.S. value-weighted industry portfolios: Oil, Banks, Textiles, Toys and Retail. Original data from Kenneth French's data library. The report uses 1927–2025 for monthly seasonality and July 1963–June 2026 for factor-model and GMM estimation.

- Calendar-month regressions; joint Wald testing; Newey–West HAC standard errors and Holm corrections (as specified in the report).
- CAPM and Fama–French five-factor return regressions for industry portfolios and momentum.
- Momentum-sorted portfolio comparisons.
- Two-step GMM estimation of a normalized CAPM SDF; Hansen J-test and a slope-restriction Wald test.

## Selected results from the report

- All five portfolios reject equal monthly means in the full-sample seasonality specification after Holm correction. Only Textiles is significant in all three subperiods. The maximal reported seasonality R² is 2.14%.
- No industry CAPM alpha is individually significant. The five-factor model increases adjusted R² for each portfolio while producing significant negative alphas for Banks, Textiles and Toys.
- The momentum alpha is approximately +0.71% monthly under CAPM and +0.75% under FF5.
- CAPM SDF: Hansen J = 4.777, p = 0.311. This is **non-rejection**, not proof that the model is correct.

## Key limitation

The five industry test assets have similar means and betas; the SDF test has limited cross-sectional power. Seasonality is unstable across subperiods and does not establish a trading strategy. Transaction costs, data snooping, time-varying exposures and joint alpha tests remain limitations.

## Reproduction status — must be addressed before public code release

The supplied original scripts and report are **not a one-command, audited reproduction package**. The factor-model script currently uses `sm.OLS(...).fit(use_t=False)`, which defaults to non-HAC covariance estimation, while the report describes HAC standard errors for factor regressions. The exported CAPM regression CSV also differs slightly from some published CAPM table entries, while the FF5 exported coefficients largely agree. Align date windows, return definitions, standard errors, tests and exported outputs; add documented dependencies and validation tests before claiming full reproducibility.

Do not publish the archived Python virtual environment, private paths or group partners' personal details as part of the code repository. Obtain co-author consent before publishing the full group report.
