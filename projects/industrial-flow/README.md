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
