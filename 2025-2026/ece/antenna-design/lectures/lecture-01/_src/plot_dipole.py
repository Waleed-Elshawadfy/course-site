"""Creates assets/dipole-pattern.png  (run:  python plot_dipole.py)"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

theta = np.linspace(1e-3, np.pi - 1e-3, 721)
F = np.abs(np.cos(np.pi / 2 * np.cos(theta)) / np.sin(theta))   # half-wave dipole
full_theta = np.concatenate([theta, -theta[::-1]])
full_F = np.concatenate([F, F[::-1]])

fig = plt.figure(figsize=(4.5, 4.5), dpi=150)
ax = fig.add_subplot(111, projection="polar")
ax.plot(full_theta, full_F, lw=2)
ax.set_theta_zero_location("N")            # dipole axis points up (theta = 0)
ax.set_theta_direction(-1)
ax.set_rticks([0.5, 1.0])
ax.set_title("Half-wave dipole (normalized)", va="bottom")
fig.tight_layout()

out = Path(__file__).resolve().parent.parent / "assets" / "dipole-pattern.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out)
print("saved", out)
