"""Self-contained, data-free public Blow control-volume illustration.

This script is independently written from standard published pipe-emptying
control-volume relationships. No experimental data, employer code, calibrated
parameters, proprietary figures or original technical report are used.

Run: python -m pip install numpy scipy matplotlib
     python projects/industrial-flow/phase4_blow_volume_demo.py
"""
from pathlib import Path
from math import pi
import numpy as np
from scipy.integrate import solve_ivp

# Hypothetical inputs; not the configuration of any real installation.
L0, diameter, density = 24.0, .15, 1000.0
p_up, p_out = 175_000.0, 101_325.0
darcy_f, K = .026, 2.5
alpha, beta, positive_stop_length = .84, .35, .30
A = pi*diameter**2/4
C = beta*(1/alpha-1)-1

def rhs(t, state):
    U, L, volume_out, volume_left = state
    length = max(L, positive_stop_length/2)
    driving = (p_up-p_out)/density
    losses = (darcy_f*length/diameter+K)*U*abs(U)/2
    return [(driving-losses+C*U*abs(U))/length,
            -U/alpha, A*U, A*U*(1/alpha-1)]

def stop(t, state):
    return state[1]-positive_stop_length

stop.terminal = True
stop.direction = -1

result = solve_ivp(rhs, (0, 60), [0,L0,0,0], method="DOP853",
                   events=stop, max_step=.05, rtol=1e-9,
                   atol=1e-11, dense_output=True)
if not result.success or not len(result.t_events[0]):
    raise RuntimeError("The safe stopping event was not reached.")

t = np.linspace(0, result.t_events[0][0], 450)
_, L, Vout, Vleft = result.sol(t)
full = A*L
initial = A*L0
if not np.allclose(full+Vout+Vleft, initial, atol=1e-8):
    raise RuntimeError("Product volume is not conserved.")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9.7,4.4), layout="constrained")
ax.plot(t, full/initial, lw=2.6, color="#467f9b", label="Full liquid column")
ax.plot(t, Vout/initial, lw=2.6, color="#24766e", label="Discharged")
ax.plot(t, Vleft/initial, lw=2.6, color="#b98666", label="Left behind")
ax.set(xlabel="Simulation time (s)", ylabel="Fraction of initial liquid volume",
       ylim=(0,1.03))
ax.grid(alpha=.25)
ax.legend(frameon=False, ncol=3)
ax.set_title("Blow transition: where the liquid goes", loc="left")
out = Path(__file__).resolve().parents[2] / "assets"
out.mkdir(exist_ok=True)
fig.savefig(out/"industrial-phase4-blow-volume-reproduced.svg", dpi=170)
plt.close(fig)
print("Completed without using any experimental or proprietary data.")
