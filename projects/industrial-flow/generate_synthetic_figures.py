"""Original, data-free mathematical illustrations for the portfolio website.

No company data, test setup or proprietary implementation is used.
The two equations are standard published physical relationships.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11, "figure.facecolor": "#f8faf8",
    "axes.facecolor": "#ffffff", "axes.edgecolor": "#dbe4e0",
    "axes.labelcolor": "#53666a", "xtick.color": "#53666a",
    "ytick.color": "#53666a", "svg.fonttype": "none",
})
TEAL = "#24766e"
BLUE = "#467f9b"
WARM = "#b98666"


def save(fig, name):
    for extension in ("svg", "png"):
        fig.savefig(OUT / f"{name}.{extension}", dpi=190, bbox_inches="tight")
    plt.close(fig)


def style(ax, title, xlabel, ylabel):
    ax.set_title(title, loc="left", fontsize=19, pad=22, color="#20343a")
    ax.set(xlabel=xlabel, ylabel=ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color="#dbe4e0", linewidth=0.8)
    ax.set_axisbelow(True)


# Polytropic pressure law for expansion of a trapped gas volume.
# All quantities are normalized; neither initial pressure nor volume is
# related to an actual industrial system.
s = np.linspace(0, 0.75, 181)  # swept volume / initial pipe volume
n = 1.2
gas_initial_fraction = 0.5
ratio = (gas_initial_fraction / (gas_initial_fraction + s)) ** n
fig, ax = plt.subplots(figsize=(10, 4.7), layout="constrained")
style(ax, "Pressure during isolated gas expansion",
      "Fraction of initial pipe volume swept by gas", "Absolute pressure / initial pressure")
ax.plot(s, ratio, color=TEAL, lw=2.7, label="Polytropic expansion")
ax.plot(s, np.ones_like(s), color=BLUE, lw=2.7, label="Constant-pressure case")
ax.set(xlim=(0, 0.75), ylim=(0, 1.2))
ax.legend(frameon=False)
save(fig, "industrial-pressure-expansion")


# Volumetric conservation for a simple moving full column plus holdup.
# beta = 0.20 is an illustrative assumption, NOT a fitted coefficient.
s = np.linspace(0, 0.9, 181)
beta = 0.20
full = 1 - s
outflow = (1 - beta) * s
holdup = beta * s
assert np.allclose(full + outflow + holdup, 1)
fig, ax = plt.subplots(figsize=(10, 4.7), layout="constrained")
style(ax, "Where the displaced product goes",
      "Fraction of initial pipe volume swept", "Fraction of initial product volume")
ax.plot(s, full, color=BLUE, lw=2.7, label="Full liquid column")
ax.plot(s, outflow, color=TEAL, lw=2.7, label="Discharged product")
ax.plot(s, holdup, color=WARM, lw=2.7, label="Liquid holdup")
ax.set(xlim=(0, 0.9), ylim=(0, 1))
ax.legend(frameon=False)
save(fig, "industrial-product-volume-balance")

print("Wrote data-free SVG and PNG figures:", OUT)
