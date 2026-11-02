# Machine learning for asset pricing

**Current project · Machine Learning / Asset pricing**

## Research question

Can regularized and nonlinear methods improve cross-sectional stock-return forecasts compared with standard linear asset-pricing baselines? If so, do forecast improvements also translate into stronger out-of-sample portfolio results?

## Project scope

The project compares conventional linear methods with regularized regression and nonlinear machine-learning models. I want to distinguish predictive accuracy from economic usefulness rather than assume that a better statistical fit automatically makes a better investment strategy.

The planned work includes:

- **Baselines:** compare a simple linear cross-sectional return model and factor-based benchmark predictions.
- **Regularization:** assess ridge, lasso and elastic-net specifications under comparable data preprocessing.
- **Nonlinear prediction:** investigate tree-based methods and other suitable nonlinear models, with attention to interactions across stock characteristics.
- **Validation:** use chronological training, validation and test periods; conduct expanding- or rolling-window evaluation without future-information leakage.
- **Statistical assessment:** compare out-of-sample forecast errors and cross-sectional predictive measures.
- **Economic assessment:** translate predicted returns into transparent portfolio sorts or allocations and compare realized returns, turnover and risk-adjusted performance.
- **Robustness:** examine sensitivity to sample splits, model tuning, feature availability, transaction costs and multiple comparisons.

These are intended experiments. No completed training results or out-of-sample performance improvements are claimed here.

## Related papers

- Gu, S., Kelly, B. & Xiu, D. (2020), [*Empirical Asset Pricing via Machine Learning*](https://doi.org/10.1093/rfs/hhaa009). Compares machine-learning methods for equity risk premia and studies the role of nonlinear predictive interactions.
- Fama, E. F. & French, K. R. (2015), [*A Five-Factor Asset Pricing Model*](https://doi.org/10.1016/j.jfineco.2014.10.010). A conventional asset-pricing benchmark against which more flexible approaches can be assessed.
- Bailey, D. H. & López de Prado, M. (2014), [*The Deflated Sharpe Ratio*](https://doi.org/10.3905/jpm.2014.40.5.094). A complementary warning about multiple testing and overstated reported strategy performance.

These papers are project references rather than a record of completed replications or readings.

[Back to Exploring & Reading](https://zorromir.github.io/#engineering)
