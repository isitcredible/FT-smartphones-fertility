"""
Visualise the FT chart's recipe: for each country, plot the actual TFR
series (from the FT chart, slide 0) alongside the OLS 11-year pre-trend
line extrapolated forward past the chart-implied take-off year.

The vertical gap between the two lines is the "% deviation from the
pre-smartphone trend" that appears in the FT's headline panel. For
countries whose pre-trend was already rising or flat (UK, Australia,
Egypt, Iran, US), the extrapolated trend continues upward; any
post-takeoff fall in actual TFR opens a large gap. For countries whose
pre-trend was already falling (Mexico, Senegal), the recipe by
construction generates almost no "shock."

Output: figures/pretrend_extrapolation.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from _style import (
    FT_CLARET, FT_OXFORD, FT_CYAN, FT_INK,
    add_brand, add_source, apply_ft_style,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

# Display order; takeoff is read from the slide-0 CSV.
# Chronological by chart-implied take-off; alphabetical within year.
ORDER = [
    ("USA", "United States"),    # 2007
    ("AUS", "Australia"),        # 2008
    ("GBR", "United Kingdom"),   # 2009
    ("IDN", "Indonesia"),        # 2012
    ("MEX", "Mexico"),           # 2013
    ("SEN", "Senegal"),          # 2013
    ("EGY", "Egypt"),            # 2014
    ("IRN", "Iran"),             # 2015
]

WINDOW = 11
FORWARD = 10

apply_ft_style()
df = pd.read_csv(DATA / "ft_chart_slide0_tfr_by_year.csv")

fig, axes = plt.subplots(2, 4, figsize=(15, 8), sharex=True)

for ax, (iso, name) in zip(axes.flatten(), ORDER):
    sub = df[df["iso3"] == iso].sort_values("year").set_index("year")
    takeoff = int(sub["takeoff"].iloc[0])
    tfr = sub["tfr"]

    # Actual TFR
    ax.plot(tfr.index, tfr.values, color=FT_CYAN, lw=2.2, zorder=2)

    # OLS pre-trend over the 11-year window (takeoff-10..takeoff)
    pre_years = np.arange(takeoff - (WINDOW - 1), takeoff + 1)
    pre = tfr.reindex(pre_years).dropna()
    slope, intercept = np.polyfit(pre.index.values, pre.values, 1)

    # Extrapolated forward
    forward_years = np.arange(takeoff, takeoff + FORWARD + 1)
    forward = intercept + slope * forward_years
    ax.plot(
        forward_years, forward,
        color=FT_CLARET, lw=1.6, ls="--", zorder=3,
        label="Extrapolated pre-trend",
    )

    # Pre-trend fitted segment
    fitted = intercept + slope * pre.index.values
    ax.plot(
        pre.index.values, fitted,
        color=FT_CLARET, lw=1.4, alpha=0.55, zorder=3,
    )

    ax.axvline(takeoff, color=FT_CLARET, lw=1.4, ls="--")
    ax.set_title(f"{name} (take-off {takeoff})")
    ax.set_xlim(1990, 2023)

axes[0, 0].set_ylabel("Births per woman")
axes[1, 0].set_ylabel("Births per woman")

fig.subplots_adjust(top=0.78, bottom=0.07, left=0.05, right=0.99, hspace=0.30, wspace=0.22)
fig.suptitle(
    "The recipe behind the FT chart",
    x=0.01, y=0.965, ha="left",
)
fig.text(
    0.01, 0.910,
    "Total fertility rate from the FT chart.",
    fontsize=13, color=FT_CYAN, fontweight="bold", ha="left",
)
fig.text(
    0.01, 0.875,
    "OLS linear fit to the 11 years up to take-off, extrapolated forward.",
    fontsize=13, color=FT_CLARET, fontweight="bold", ha="left",
)
fig.text(
    0.01, 0.840,
    "The FT’s “% deviation” is the gap between these two lines after take-off.",
    fontsize=12, color="#555555", ha="left",
)
add_source(
    fig,
    "Source: TFR series extracted from the FT scrollytelling SVG; "
    "11-year linear pre-trend fitted. The Catalogue of Errors Ltd.",
)
add_brand(fig)
fig.savefig(FIG / "pretrend_extrapolation.png")
print(f"Wrote {FIG / 'pretrend_extrapolation.png'}")
