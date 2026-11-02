# Machine learning for asset pricing

**Current project · Machine Learning / Asset pricing**

## Research question

Can regularized and nonlinear methods improve cross-sectional stock-return forecasts compared with standard linear asset-pricing baselines? If so, do forecast improvements also translate into stronger out-of-sample portfolio results?

## Project scope

In this project, I will investigate whether machine-learning methods can improve cross-sectional stock-return prediction compared with conventional linear asset-pricing models.

The analysis will begin with simple, interpretable benchmarks before introducing additional model complexity. I will first compare OLS with Ridge, LASSO and Elastic Net. The project will then examine explicit nonlinearities and interactions before moving to tree-based models, gradient boosting and possibly neural networks. I will see how far I get, since the full scope may be too broad for one project.

All models will use the same dataset and chronological training, validation and test samples. Performance will be evaluated not only through forecast errors and out-of-sample $R^2$, but also through ranking ability, portfolio returns, Sharpe ratios, drawdowns, turnover, transaction costs and conventional factor-adjusted alpha.

A central question is whether machine learning discovers new return structure or mainly learns nonlinear combinations of familiar characteristics such as value, momentum, size, profitability and volatility.

The project therefore focuses as much on validation and interpretation as on predictive performance. Once the initial analysis is complete, I plan to extend it using the papers I have been reading on reliable backtesting.

### Planned stages

1. Construct a point-in-time stock-characteristic dataset.
2. Establish OLS and historical-mean benchmarks.
3. Compare Ridge, LASSO and Elastic Net.
4. Add explicit nonlinear terms and characteristic interactions.
5. Estimate Random Forest and gradient-boosted tree models.
6. Introduce a neural-network benchmark only after simpler models are understood.
7. Compare statistical forecast performance.
8. Form portfolios from predicted returns and evaluate economic performance.
9. Measure turnover and transaction-cost sensitivity.
10. Analyse feature importance, interactions and factor exposures.
11. Test robustness across different periods and markets.

### Main research references

- Gu, Kelly & Xiu — [*Empirical Asset Pricing via Machine Learning*](https://doi.org/10.1093/rfs/hhaa009).
- Cakici, Fieberg, Metko & Zaremba — [*Machine Learning Goes Global: Cross-Sectional Return Predictability in International Stock Markets*](https://doi.org/10.1016/j.jedc.2023.104725).
- Drobetz & Otto — [*Empirical Asset Pricing via Machine Learning: Evidence from the European Stock Market*](https://doi.org/10.1057/s41260-021-00237-x).
- Bailey, Borwein, López de Prado & Zhu — [*The Probability of Backtest Overfitting*](https://doi.org/10.21314/JCF.2016.322).
- Bailey & López de Prado — [*The Deflated Sharpe Ratio*](https://doi.org/10.3905/jpm.2014.40.5.094).

These papers guide the research. The project plan does not imply that the models, empirical comparisons or backtesting extensions have already been completed.

[Back to Exploring & Reading](https://zorromir.github.io/#engineering)
