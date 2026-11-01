"""Stand-alone data-free Phase 3 example.

Independent example based on standard Darcy-Weisbach single-phase relations.
All parameters are invented. No industrial equipment or test data are used.

Run:
    python -m pip install numpy matplotlib
    python projects/industrial-flow/phase3_pipe_resistance_demo.py
"""
from math import pi, sqrt
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

# Consecutive hypothetical pipe lengths [m], internal diameters [m],
# downstream local K coefficients and elevations [m].
lengths = np.array([20.0, 35.0, 25.0])
diameters = np.array([0.16, 0.11, 0.14])
local_ks = np.array([1.2, 2.0, 0.8])
area = pi * diameters**2 / 4
rho, darcy = 998.0, 0.024
total_length = lengths.sum()
d_equivalent = sqrt(4 * np.dot(lengths, area) / (pi * total_length))
area_equivalent = pi*d_equivalent**2/4

def flow_dependent_loss_pa(q_m3_s):
    """Return friction + local head losses, excluding static elevation."""
    speeds = q_m3_s / area
    segment_losses = (darcy*lengths/diameters + local_ks)*rho*speeds**2/2
    equivalent_speed = q_m3_s / area_equivalent
    equivalent_loss = (
        darcy*total_length/d_equivalent + local_ks.sum()
    )*rho*equivalent_speed**2/2
    return segment_losses.sum(), equivalent_loss

flow_lps = np.linspace(0, 11, 160)
two_cases = np.array([flow_dependent_loss_pa(q/1000) for q in flow_lps])/1000
fig, ax = plt.subplots(figsize=(10, 4.8), layout="constrained")
ax.plot(flow_lps, two_cases[:, 0], label="Three pipe segments", color="#24766e", linewidth=2.7)
ax.plot(flow_lps, two_cases[:, 1], label="Volume-equivalent pipe",
        color="#467f9b", linewidth=2.7, linestyle="--")
ax.set(xlabel="Volumetric flow (L/s)", ylabel="Friction + local losses (kPa)")
ax.set_title("Equal volume does not mean equal resistance", loc="left")
ax.grid(color="#dbe4e0")
ax.legend(frameon=False)
fig.savefig(OUT / "industrial-phase3-resistance-reproduced.svg")
plt.close(fig)
