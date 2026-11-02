"""Creates assets/ni-vs-temperature.png  (run:  python plot_ni.py)"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

k = 8.617333e-5          # Boltzmann constant, eV/K
Eg = 1.12                # eV (held constant: approximation)
T = np.linspace(250, 450, 200)
ni = 1.0e10 * (T / 300) ** 1.5 * np.exp(-Eg / (2 * k) * (1 / T - 1 / 300))

fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
ax.semilogy(T, ni, lw=2)
ax.axvline(300, ls="--", color="gray")
ax.text(303, ni.min() * 1.5, "300 K", color="gray")
ax.set_xlabel("Temperature (K)")
ax.set_ylabel(r"$n_i$ (cm$^{-3}$)")
ax.set_title("Silicon: intrinsic carrier concentration (approx.)")
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()

out = Path(__file__).resolve().parent.parent / "assets" / "ni-vs-temperature.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out)
print("saved", out)
