"""Independent illustrative Rinse -> Dry mass-balance example.
No proprietary source code or experimental data are used.

Install: python -m pip install numpy scipy matplotlib
Run: python phase6_rinse_dry_demo.py
"""
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Invented well-mixed compartment inputs; not real pipe geometry.
N, WATER_FLOW, GOAL, MIXING_VOLUME, DETACH_RATE = 3, .8, 48., 12., .025
initial_wall = np.array([.8,.6,.4])
initial_mobile = np.array([.05,.03,.02])
exchange_rate = WATER_FLOW/MIXING_VOLUME
start = np.r_[np.zeros(N), initial_mobile, initial_wall, np.zeros(3)]

def rhs(t,y):
    w,m,b=y[:N],y[N:2*N],y[2*N:3*N]
    q_w=exchange_rate*w
    q_m=exchange_rate*m
    detached=DETACH_RATE*b
    return np.r_[
        np.r_[WATER_FLOW,q_w[:-1]]-q_w,
        np.r_[0.,q_m[:-1]]-q_m+detached,
        -detached,
        [WATER_FLOW,q_w[-1],q_m[-1]]
    ]

stop_time=GOAL/WATER_FLOW
t_rinse=np.linspace(0,stop_time,451)
sol=solve_ivp(rhs,(0,stop_time),start,t_eval=t_rinse,
              rtol=1e-10,atol=1e-12,method="DOP853")
if not sol.success:
    raise RuntimeError(sol.message)
water=sol.y[:N].sum(axis=0)
product=sol.y[N:3*N].sum(axis=0)
injected,outwater,outproduct=sol.y[3*N:]
assert np.max(np.abs(injected-water-outwater))<1e-8
assert np.max(np.abs(initial_wall.sum()+initial_mobile.sum()-product-outproduct))<1e-8

# Explicit transfer, not a coupled compressor or drying-physics solver.
dry_water_0=float(water[-1])
dry_rate=.026  # invented rate; NOT tied to compressor flow
dry_target=.90 # invented water-removal fraction, NOT a verified dryness standard
dry_duration=-np.log(1-dry_target)/dry_rate
t_dry=np.linspace(0,dry_duration,451)
water_dry=dry_water_0*np.exp(-dry_rate*t_dry)
assert np.max(np.abs(water_dry+(dry_water_0-water_dry)-dry_water_0))<1e-8
assert water_dry[0]==dry_water_0

fig,ax=plt.subplots(figsize=(10,4.6),layout="constrained")
ax.plot(t_rinse,water,color="#467f9b",lw=2.7,label="Rinse: water in pipe")
ax.plot(stop_time+t_dry,water_dry,color="#24766e",lw=2.7,
        label="Dry: hypothetical first-order removal")
ax.axvline(stop_time,color="#b98666",ls="--",lw=1.5,label="Rinse to Dry")
ax.set(title="Rinse to Dry: remaining water in the pipe",
       xlabel="Time since start of Rinse (s)",ylabel="Water inventory (L)")
ax.spines[["top","right"]].set_visible(False)
ax.grid(alpha=.22)
ax.legend(frameon=False)
output=Path(__file__).with_name("phase6-rinse-dry-reproduced.svg")
fig.savefig(output,bbox_inches="tight")
print("Rinse completion (s):", stop_time)
print("Water handed to Dry (L):", dry_water_0)
print("Dry elapsed time (s):", dry_duration)
print("Water after Dry (L):", water_dry[-1])
print("Saved:",output)
