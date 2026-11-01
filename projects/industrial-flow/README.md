# Industrial pipeline modelling — public examples

Small public demonstrations of published fluid-mechanics equations, written to accompany the [portfolio case study](https://zorromir.github.io/#projects). The [standalone pipeline-flow repository](https://github.com/zorromir/pipeline-flow-modelling) is now published with a modular Python package, tests, five example figures and modelling notes. That repository explicitly documents its AI-assisted reconstruction of selected methods.

All inputs are **synthetic**. There are no employer datasets, internal reports, calibrated parameters, installation diagrams or original company source files here.

## Reproducible examples

| Topic | Code |
| --- | --- |
| Polytropic pressure and product-volume balances | [Basic figures](generate_synthetic_figures.py) |
| Air-driven moving-column dynamics | [Push numerical example](rigid_column_example.py) |
| Segmented versus volume-equivalent pipe | [Pipeline resistance](phase3_pipe_resistance_demo.py) |
| Control-volume balance in Blow | [Blow transition](phase4_blow_volume_demo.py) |
| Scrambled Sobol sampling, simulated Push uncertainty | [QMC example](phase5_qmc_push_demo.py) |
| Rinse-to-Dry water inventory transfer | [Rinse / Dry example](phase6_rinse_dry_demo.py) |

Install NumPy, SciPy and Matplotlib, then run a script with Python. These examples are designed to be self-contained and not to read industrial measurements.

## What the figures establish

The examples illustrate model behaviour and numerical consistency, **not** experimental predictive accuracy. The Blow model is not a validated annular-flow simulator; Rinse and Dry are simplified mass-balance and inventory examples. Sobol sampling is a space-filling input design here, not a computation of variance-based Sobol indices.

## Research references

- Tijsseling et al. (2016), *Improved One-Dimensional Models for Rapid Emptying and Filling of Pipelines* — https://doi.org/10.1115/1.4031508
- Chen et al. (2024), *Experimental data on filling and emptying of a large-scale pipeline* — https://doi.org/10.1038/s41597-024-03441-7

The publications are external scientific sources, not work authored by the portfolio owner. Source-code reuse and publication of further industrial material require the relevant permissions.

**Publication status:** This directory contains small standalone examples retained for the website. The dedicated [pipeline-flow-modelling](https://github.com/zorromir/pipeline-flow-modelling) repository is the main public demonstration. Neither source is the original industrial codebase, and neither validates performance against confidential measurements.
