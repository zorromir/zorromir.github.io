"""A small Monte Carlo experiment with panel-data estimators.
Run: pip install numpy matplotlib
     python panel_monte_carlo_minimal.py
Saves two plots next to this file.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(2026)
N, T, R = 200, 5, 1000

def slope(x, y):
    x = x - x.mean(axis=(1, 2), keepdims=True)
    y = y - y.mean(axis=(1, 2), keepdims=True)
    return (x * y).sum(axis=(1, 2)) / (x * x).sum(axis=(1, 2))

a = rng.normal(size=(R, N, 1))
x = rng.normal(size=(R, N, T)) + 0.5 * a
u = rng.normal(size=(R, N, T)).cumsum(axis=2)
y = 1 + a + 2 * x + u

pooled = slope(x, y)
fe = slope(x - x.mean(axis=2, keepdims=True),
           y - y.mean(axis=2, keepdims=True))
dx, dy = np.diff(x, axis=2), np.diff(y, axis=2)
fd = (dx * dy).sum(axis=(1, 2)) / (dx * dx).sum(axis=(1, 2))

print('Estimator         Mean     SD     Bias')
for name, b in [('Pooled OLS', pooled), ('Fixed effects', fe), ('First differences', fd)]:
    print(f'{name:18s} {b.mean():.3f}   {b.std(ddof=1):.3f}   {b.mean()-2:+.3f}')

plt.figure(figsize=(6.2, 3.1))
plt.boxplot([pooled, fe, fd], tick_labels=['Pooled OLS', 'FE', 'FD'], showfliers=False)
plt.axhline(2, linestyle='--', linewidth=1, label='True slope = 2')
plt.ylabel('Estimated slope')
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig(OUT / 'panel_estimates.png', dpi=180)
plt.close()

periods = [5, 10, 20, 50]
means = []
for t in periods:
    a = rng.normal(size=(R, N, 1))
    x = rng.normal(size=(R, N, t)) + 0.5 * a
    u = rng.normal(size=(R, N, t)).cumsum(axis=2)
    y = np.empty_like(x)
    y[:, :, 0] = 1 + a[:, :, 0] + 2*x[:, :, 0] + u[:, :, 0]
    for k in range(1, t):
        y[:, :, k] = 1 + a[:, :, 0] + 2*x[:, :, k] + 0.5*y[:, :, k-1] + u[:, :, k]

    within = lambda z: z - z.mean(axis=2, keepdims=True)
    response = within(y[:, :, 1:])
    lag = within(y[:, :, :-1])
    regressor = within(x[:, :, 1:])
    ll = (lag * lag).sum(axis=(1, 2))
    xx = (regressor * regressor).sum(axis=(1, 2))
    lx = (lag * regressor).sum(axis=(1, 2))
    ly = (lag * response).sum(axis=(1, 2))
    xy = (regressor * response).sum(axis=(1, 2))
    rho_hat = (ly * xx - xy * lx) / (ll * xx - lx**2)
    means.append(rho_hat.mean())
    print(f'T = {t:2d}: mean estimated rho = {rho_hat.mean():.3f}')

plt.figure(figsize=(6.2, 3.1))
plt.plot(periods, means, marker='o', label='Mean FE estimate')
plt.axhline(0.5, linestyle='--', linewidth=1, label='True rho = 0.5')
plt.xticks(periods)
plt.xlabel('Periods per individual (T)')
plt.ylabel('Estimated persistence')
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig(OUT / 'panel_dynamic.png', dpi=180)
plt.close()
