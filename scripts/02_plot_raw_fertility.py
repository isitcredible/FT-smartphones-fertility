"""
Plot raw TFR series, 1990-2023, for each of Burn-Murdoch's eight countries,
with the FT-stated 'smartphone take-off' year marked.

Output: figures/raw_fertility_rates.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

FT = {
    "USA": ("United States", 2007),
    "GBR": ("United Kingdom", 2007),
    "AUS": ("Australia", 2007),
    "MEX": ("Mexico", 2012),
    "IDN": ("Indonesia", 2012),
    "IRN": ("Iran", 2015),
    "EGY": ("Egypt", 2015),
    "SEN": ("Senegal", 2015),
}

tfr = pd.read_csv(DATA / "tfr_annual.csv")

fig, axes = plt.subplots(2, 4, figsize=(14, 7), sharex=True)
for ax, (iso, (name, t)) in zip(axes.flatten(), FT.items()):
    s = tfr[tfr["iso3"] == iso].set_index("year")["TFR"].loc[1990:2023]
    ax.plot(s.index, s.values, color="steelblue")
    ax.axvline(t, color="red", lw=1, ls="--", label=f"FT takeoff {t}")
    ax.set_title(name)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, frameon=False)

fig.suptitle("Raw total fertility rate with FT's stated 'smartphone take-off' year")
fig.supylabel("TFR (births per woman)")
fig.tight_layout()
fig.savefig(FIG / "raw_fertility_rates.png", dpi=160)
print(f"Wrote {FIG / 'raw_fertility_rates.png'}")
