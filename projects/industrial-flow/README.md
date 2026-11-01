# Industrial pipeline modelling — public mathematical figures

This directory contains **independent, data-free illustrations** of the physical relationships described in an industrial modelling case study. It contains **no original employer source code**, factory measurements, experimental sensor series, pipe layouts, calibration parameters, or internal technical report.

## What the figures show

- **Pressure under isolated gas expansion:** an ideal-gas/polytropic source \(p/p_0=(V_{g,0}/V_g)^n\), plotted alongside an idealized constant-pressure boundary. The two assumptions describe *different* possible source models, not one fitted experimental run.
- **Product-volume bookkeeping:** \(V_{\mathrm{full}}+V_{\mathrm{holdup}}+V_{\mathrm{out}}=V_0\), where \(V_{\mathrm{holdup}}=\beta V_{\mathrm{pass}}\), \(V_{\mathrm{out}}=(1-\beta)V_{\mathrm{pass}}\).
- Other plots shown on the portfolio use an independently written constant-pressure moving-column numerical example following Tijsseling et al. (2016).

Parameters are deliberately hypothetical and are **not** measured or calibrated values. Curves are illustrations, not validation results or reliable performance forecasts. These examples do not implement the full four-stage industrial application.

## Generate

```bash
python -m pip install numpy scipy matplotlib
python generate_synthetic_figures.py
python rigid_column_example.py
```

The scripts write SVG and PNG files to a local `figures/` directory. `rigid_column_example.py` integrates the published constant-pressure special case numerically and stops before the zero-length singularity. Neither script reads any dataset.

## Scientific references

Tijsseling, Hou, Bozkus & Laanearu (2016), *Improved One-Dimensional Models for Rapid Emptying and Filling of Pipelines*, [DOI](https://doi.org/10.1115/1.4031508).

Chen, Hou, Laanearu & Tijsseling (2024), *Experimental data on filling and emptying of a large-scale pipeline*, [DOI](https://doi.org/10.1038/s41597-024-03441-7). Its experiment data are **not** included in these plots.

These sources describe the relevant research concepts. They do not validate this simplified demonstration.

## Phase 4: Blow control-volume demonstration

The [Phase 4 standalone Python example](phase4_blow_volume_demo.py) solves a simplified, constant-pressure Blow transition and plots the conserved liquid volumes. Inputs are synthetic. This is **not** an annular-flow correlation, a film-stripping calibration or a validated cleaning prediction.

Full Phase 4 transition and separated film-inventory models are prepared in the local `pipeline-flow-modelling` package pending a dedicated public repository. No company records are included.

## Phase 5: uncertainty propagation using synthetic Sobol scenarios

The [Phase 5 Python reproducer](phase5_qmc_push_demo.py) numerically integrates the independent uniform-pipe Push equations for 256 **scrambled Sobol** parameter combinations. It varies four deliberately invented inputs — initial air pressure, Darcy friction, outlet resistance and liquid holdup — and produces a percentile envelope for simulated outlet product flow at matched removal progress.

Run it with:

```bash
python -m pip install numpy scipy matplotlib
python phase5_qmc_push_demo.py
```

The median simulated time to reach 50% product removal is approximately 10.30 s (10th–90th sample percentiles: 8.61–12.45 s) for this **hypothetical scenario design**. These are *sample quantiles*, not validated confidence or prediction intervals. Sobol points are used to sample the inputs; the project does not claim variance-based Sobol sensitivity indices.

The complete modular uncertainty implementation, tests, and additional figures are in the local, standalone `pipeline-flow-modelling` Phase 5 package until a dedicated public repository is available.
