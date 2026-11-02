# Fama–French factor extensions

**Current project · Asset pricing / Quantitative research**

## Research question

Do published refinements to value, momentum and low-volatility signals contain information beyond established Fama–French factors, and do any apparent improvements survive out-of-sample evaluation?

## Project scope

The idea behind this project is to reproduce the standard Fama–French asset-pricing models and investigate extensions that could improve the robustness of traditional factors.

I will first look at the basic CAPM, Fama–French three-factor, five-factor and momentum benchmarks. After that, I will study three extensions: enhanced value measures beyond book-to-market, residual momentum based on stock-specific returns, and a low-volatility factor. Each extension will be tested separately before being combined with the standard model.

The empirical analysis will compare models using factor-spanning regressions, pricing errors, HAC inference, factor correlations, drawdowns and out-of-sample performance. I also want to investigate data leakage, survivorship bias, multiple testing and the distinction between in-sample fit and genuine predictive improvement, although these checks may be too much for the initial scope.

The broader objective is to understand whether these modifications contain additional information beyond the standard Fama–French models, rather than simply constructing a model with more factors.

### Planned stages

1. Reproduce CAPM, FF3, FF5 and FF5 + momentum.
2. Reproduce conventional value and momentum factors.
3. Construct enhanced value, residual momentum and low-volatility signals.
4. Test whether the new factors are spanned by existing factors.
5. Compare nested factor-model specifications.
6. Evaluate stability across subperiods and out-of-sample data.
7. Investigate a later nonlinear or machine-learning extension.

### Main research references

- Fama & French — [*A Five-Factor Asset Pricing Model*](https://doi.org/10.1016/j.jfineco.2014.10.010).
- Blitz & Hanauer — [*Resurrecting the Value Premium*](https://ssrn.com/abstract=3705218).
- Blitz, Huij & Martens — [*Residual Momentum*](https://doi.org/10.1016/j.jempfin.2011.01.003).
- Blitz & van Vliet — [*The Volatility Effect: Lower Risk Without Lower Return*](https://ssrn.com/abstract=980865).
- Blitz & Hanauer — [*Settling the Size Matter*](https://ssrn.com/abstract=3686583).

These are papers guiding the project, not completed replications or verified empirical findings.

[Back to Exploring & Reading](https://zorromir.github.io/#engineering)
