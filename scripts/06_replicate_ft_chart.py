"""
Canonical replication of the FT chart: % change in TFR relative to a
pre-smartphone trend, by years before/since the FT-stated 'smartphone
take-off' year. The pre-trend is a log-linear fit to the five years
immediately before each country's take-off year.

Output: figures/replication.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
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

PALETTE = ["#005ab5", "#00838f", "#003f5c", "#bc5090",
          "#e07a5f", "#ef7d00", "#d62728", "#8c564b"]

WINDOW = 5
HORIZON = (-10, 16)

tfr = pd.read_csv(DATA / "tfr_annual.csv")


def deviation(iso3, takeoff):
    s = tfr[tfr["iso3"] == iso3].set_index("year")["TFR"].sort_index()
    pre_years = np.arange(takeoff - WINDOW, takeoff)
    pre = s.reindex(pre_years).dropna()
    slope, intercept = np.polyfit(pre.index.values, np.log(pre.values), 1)
    event_years = np.arange(takeoff + HORIZON[0], takeoff + HORIZON[1] + 1)
    actual = s.reindex(event_years).values
    predicted = np.exp(intercept + slope * event_years)
    return event_years - takeoff, 100 * (actual / predicted - 1)


fig, ax = plt.subplots(figsize=(9, 6))
for (iso, (name, t)), color in zip(FT.items(), PALETTE):
    et, dev = deviation(iso, t)
    ax.plot(et, dev, color=color, lw=2.0, label=name)

ax.axhline(0, color="black", lw=0.7)
ax.axvline(0, color="black", lw=0.7, ls="--", alpha=0.6)
ax.set_xlabel("Years before / since 'smartphone take-off'")
ax.set_ylabel("% change in TFR vs pre-smartphone trend")
ax.set_title("Replicating the FT chart\n"
             "(5-year log-linear pre-trend, FT-stated take-off years)")
ax.legend(loc="lower left", fontsize=9, frameon=False)
ax.grid(alpha=0.3)
ax.set_xlim(HORIZON)
fig.tight_layout()
fig.savefig(FIG / "replication.png", dpi=160)
print(f"Wrote {FIG / 'replication.png'}")
