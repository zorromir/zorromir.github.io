"""Independent numerical reproduction of a published 1D pipe-emptying model.

The input values are invented and are not industrial measurements or calibration.
Reference: Tijsseling et al. (2016), DOI 10.1115/1.4031508, eq. (9).
"""
from dataclasses import dataclass, replace
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
COLORS = ["#467f9b", "#24766e", "#b98666"]

@dataclass(frozen=True)
class Parameters:
    initial_liquid_length_m: float = 100.0
    pipe_diameter_m: float = 0.20
    density_kg_m3: float = 1000.0
    imposed_delta_p_pa: float = 40000.0
    darcy_factor: float = 0.020
    local_loss_coefficient: float = 4.0
    holdup_fraction: float = 0.20

def run(p: Parameters, stop_length_m=5.0):
    """Solve only while the rigid liquid column has nonzero safe length."""
    b = p.holdup_fraction
    if not (0 <= b < 1):
        raise ValueError("holdup_fraction outside [0,1)")
    area = np.pi * (p.pipe_diameter_m/2)**2

    def rhs(t, y):
        v, length = y
        if length <= 0:
            return [0., 0.]
        friction = (p.darcy_factor/(2*p.pipe_diameter_m)) * (
            1-b + b*b/3) * length * v*v
        outlet_loss = (p.local_loss_coefficient/2)*(1-b)**2*v*v
        drive = p.imposed_delta_p_pa/p.density_kg_m3
        dv_dt = (b*(1-b)*v*v + drive - friction - outlet_loss) / (
            (1-b/2)*length)
        return [dv_dt, -v]

    def stop(t,y):
        return y[1] - stop_length_m
    stop.terminal = True
    stop.direction = -1

    sol = solve_ivp(rhs, (0,100), [0,p.initial_liquid_length_m],
                    events=stop, max_step=.04, rtol=1e-9, atol=1e-10,
                    dense_output=True)
    if not sol.success or not len(sol.t_events[0]):
        raise RuntimeError("Safe stopping event was not reached")
    t = np.linspace(0,float(sol.t_events[0][0]),320)
    speed, length = sol.sol(t)
    if np.min(length)<0:
        raise RuntimeError("Negative liquid length")
    out_speed=(1-b)*speed
    out_flow_lps = 1000*area*out_speed
    return t,speed,out_speed,length,out_flow_lps

def axes(title,ylabel):
    fig,ax=plt.subplots(figsize=(9.8,4.4),layout="constrained")
    ax.set_title(title,fontsize=18,loc="left",color="#20343a")
    ax.set_xlabel("Simulation time (s)")
    ax.set_ylabel(ylabel)
    ax.grid(color="#dbe4e0")
    ax.set_axisbelow(True)
    ax.spines[["top","right"]].set_visible(False)
    return fig,ax

def save(fig,name):
    for suffix in ("svg","png"):
        fig.savefig(OUT / (name+"."+suffix),dpi=180,bbox_inches="tight")
    plt.close(fig)

def main():
    p=Parameters()
    t,speed,out_speed,L,Q = run(p)
    fig,ax=axes("Liquid-column velocities","Velocity (m/s)")
    ax.plot(t,speed,label="Interface velocity",color=COLORS[0],lw=2.6)
    ax.plot(t,out_speed,label="Outlet velocity",color=COLORS[1],lw=2.6)
    ax.legend(frameon=False)
    save(fig,"industrial-model-velocities")

    fig,ax=axes("Remaining liquid-column length","Column length (m)")
    ax.plot(t,L,color=COLORS[1],lw=2.6)
    save(fig,"industrial-model-column")

    fig,ax=axes("Resistance sensitivity","Discharge (L/s)")
    for k,color in zip([2,4,8],COLORS):
        tk,_,_,_,qk=run(replace(p,local_loss_coefficient=k))
        ax.plot(tk,qk,color=color,lw=2.6,label="Local loss K = "+str(k))
    ax.legend(frameon=False)
    save(fig,"industrial-model-resistance")

if __name__=="__main__":
    main()
