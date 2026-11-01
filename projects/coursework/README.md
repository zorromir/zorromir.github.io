# Current MSc coursework projects

These are project outlines based on course assignment briefs. They describe methods and questions I am working through, **not finished results or original published research**. Assignment datasets and full assessed solutions are not distributed through this portfolio.

## Panel-data estimation and dynamic models

**Course:** Panel Data Analysis of Microeconomic Decisions · Fall 2026

I am studying how to identify causal effects when individuals are observed repeatedly and have unobserved characteristics. The assignment starts with a simulated data-generating process and uses repeated Monte Carlo samples to compare estimators and standard errors.

**Focus**
- Pooled OLS bias when an explanatory variable is correlated with unobserved individual effects
- Cluster-robust standard errors and the consequences of serial dependence
- Fixed effects, first differences, and random effects
- Grouped fixed effects and time-varying unobserved heterogeneity
- Dynamic-panel bias and the Arellano–Bond approach to instrumental variables

The assignment uses **Stata**. Numerical results and conclusions should be added only after they have been produced and checked.

## Stochastic interest rates and derivative pricing

**Course:** Valuation and Risk Management · Fall 2026

This assignment studies pricing in a market with two risky assets and a stochastic short rate driven by an additional Brownian source of risk.

**Focus**
- Absence of arbitrage versus market completeness
- Contingent-claim pricing PDEs and hedging of interest-rate risk
- Short-rate dynamics of Cox–Ingersoll–Ross type
- Risk premia, pricing kernels and calibration under the real-world and risk-neutral measures
- Constructing zero-coupon yield, discount and forward curves from DNB pension-fund data
- Calibrating the **Vasicek** and **Nelson–Siegel** term-structure models, simulating rates, and pricing bond options

This is a project scope, not a claim that the model calibration or option-pricing results have been completed. The assignment references a separate DNB spreadsheet.

## Supplier decisions under uncertainty

**Course:** Decision Making Under Uncertainty · Fall 2026–2027

The goal is to choose quantities from multiple suppliers when demand is uncertain and suppliers may deliver only a fraction of the order. The base problem is a multi-supplier newsvendor model with unreliable delivery.

**Focus**
- Implementing the **preference-order-based supplier selection algorithm**
- Monte Carlo estimation of profit and confidence intervals, including control variates and antithetic demand
- Stress testing correlated disruptions, increased demand and emergency spot-market procurement
- Two-stage stochastic programming and sample-average approximation (SAA)
- Comparing expected-profit objectives with **VaR** constraints and **CVaR** objectives
- Mean–MAD and mean–variance distributionally robust optimization, including an LP and a Scarf-based SOCP approximation

**Current reading:** Merzifonluoglu, Bakal, Versteeg and den Hollander (2026), *Managing unreliable suppliers under varying risk preferences: all-or-nothing versus fractional delivery guarantees*, OR Spectrum. https://doi.org/10.1007/s00291-026-00869-8

The paper's theoretical results are the authors' findings, not results from my assignment.

## Hedging and pricing hybrid insurance claims

**Course:** Risk & Regulation · Assignment specification dated 2025

This exercise considers a portfolio of stock-index-linked death-benefit contracts. The challenge is to distinguish market-hedgeable cash flows from residual insurance risk and understand how this separation affects contract pricing.

**Focus**
- Deriving a residual claim stream for a **period-by-period minimum-variance hedge**
- Comparing that hedge to a strategy rebalanced as new information becomes available
- Simulating survival, deaths and stock-index returns across a multi-period horizon
- Determining the market value of the hedgeable portion and the risk margin on the residual portion
- Applying **40% expected shortfall** and **Euler allocation** to contract-level capital/risk margins
- Quantifying diversification when male and female policies are pooled rather than separated

The source is labelled **2025**, and this entry describes continued study of that assignment framework rather than representing it as a new 2026 assignment.

---

These notes describe the academic scope of the work. No original assignment PDFs, confidential datasets, or unverified empirical outcomes are published here.
