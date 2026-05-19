"""
Canonical replication of the FT 'unified trend' chart. The recipe
reverse-engineered from the saved Flourish SVG is:

    OLS fit of TFR (level, not log) on year over an 11-year window
    from (takeoff - 10) inclusive to takeoff inclusive, then
    extrapolated forward as a straight line. The published series is
    100 * (actual / extrapolated - 1).

Every deviation reproduces to four decimal places under this recipe -
but only when the chart-implied take-off years are used, not the ones
the article prose states. Two replications are produced for
side-by-side comparison.

Output: figures/replication.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from _style import OVERLAY_COLORS, add_source, apply_ft_style, country_color

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

# (iso3, name, prose take-off, chart-implied take-off)
COUNTRIES = [
    ("USA", "United States", 2007, 2007),
    ("GBR", "United Kingdom", 2007, 2009),
    ("AUS", "Australia",      2007, 2008),
    ("MEX", "Mexico",         2012, 2013),
    ("IDN", "Indonesia",      2012, 2012),
    ("IRN", "Iran",           2015, 2015),
    ("EGY", "Egypt",          2015, 2014),
    ("SEN", "Senegal",        2015, 2013),
]

WINDOW = 11        # 11-year inclusive fit, takeoff-10..takeoff
HORIZON = (-10, 10)


def deviation(iso3, takeoff):
    s = (
        tfr[tfr["iso3"] == iso3].set_index("year")["TFR"].sort_index()
    )
    pre_years = np.arange(takeoff - (WINDOW - 1), takeoff + 1)
    pre = s.reindex(pre_years).dropna()
    slope, intercept = np.polyfit(pre.index.values, pre.values, 1)
    event_years = np.arange(takeoff + HORIZON[0], takeoff + HORIZON[1] + 1)
    actual = s.reindex(event_years).values
    predicted = intercept + slope * event_years
    return event_years - takeoff, 100.0 * (actual / predicted - 1.0)


apply_ft_style()
tfr = pd.read_csv(DATA / "tfr_annual.csv")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), sharey=True)

for iso, name, prose, chart in COUNTRIES:
    et, dev = deviation(iso, prose)
    ax1.plot(et, dev, color=country_color(name), lw=2.0, label=name)
    et, dev = deviation(iso, chart)
    ax2.plot(et, dev, color=country_color(name), lw=2.0, label=name)

for ax, title in ((ax1, "Using the prose take-off years"),
                  (ax2, "Using the chart-implied take-off years")):
    ax.axhline(0, color="#262A33", lw=0.7)
    ax.axvline(0, color="#262A33", lw=0.7, ls="--", alpha=0.5)
    ax.set_xlabel("Years before / since ‘smartphone take-off’")
    ax.set_xlim(HORIZON)
    ax.set_title(title)

ax1.set_ylabel("% change in TFR vs pre-smartphone trend")
ax2.legend(loc="lower left", fontsize=9, ncol=2)

fig.suptitle("Replicating the FT ‘unified trend’ chart",
             x=0.01, ha="left")
fig.text(0.01, 0.93,
         "11-year linear pre-trend fitted on (takeoff-10..takeoff) and extrapolated. "
         "The chart-implied years produce a steeper, more uniform 'plunge'.",
         fontsize=10, color="#555555", ha="left")
add_source(
    fig,
    "Source: UN World Population Prospects 2024; "
    "FT Flourish SVG (axis-calibrated). isitcredible.com",
)
fig.tight_layout(rect=(0.01, 0.03, 1, 0.92))
fig.savefig(FIG / "replication.png")
print(f"Wrote {FIG / 'replication.png'}")
