"""
Mexico in the FT chart's own format. Two series are plotted, both
processed through the FT’s published recipe (OLS linear fit to TFR over
the eleven years ending at the chart-implied 2013 take-off, extrapolated
forward, deviation = 100 * (actual / predicted - 1)):

  - the Mexico series the FT chart actually renders (extracted from the
    saved Flourish SVG)
  - the UN World Population Prospects 2024 series, which is the source
    the FT uses for its other seven countries

The first reproduces the FT’s headline plunge for Mexico to about
-21 per cent by year +10. The second hugs zero. Applying the FT’s own
recipe to the right data makes Mexico's "smartphone shock" disappear.

Output: figures/mexico_chart_vs_wpp.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from _style import FT_CLARET, FT_INK, FT_OXFORD, add_brand, add_source, apply_ft_style, country_color

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

TAKEOFF = 2013
WINDOW = 11   # OLS fit window: (takeoff - 10) inclusive .. takeoff inclusive


def recipe_deviation(series: pd.Series, takeoff: int) -> pd.DataFrame:
    """Return event_time and % deviation under the FT recipe."""
    pre_years = np.arange(takeoff - (WINDOW - 1), takeoff + 1)
    pre = series.reindex(pre_years).dropna()
    slope, intercept = np.polyfit(pre.index.values, pre.values, 1)
    event_years = series.index.values
    predicted = intercept + slope * event_years
    return pd.DataFrame({
        "event_time": event_years - takeoff,
        "year": event_years,
        "pct_deviation": 100.0 * (series.values / predicted - 1.0),
    })


apply_ft_style()
mex = pd.read_csv(DATA / "mexico_chart_vs_wpp.csv").set_index("year").sort_index()

dev_chart = recipe_deviation(mex["tfr_chart"], TAKEOFF)
dev_wpp = recipe_deviation(mex["tfr_wpp"], TAKEOFF)

fig, ax = plt.subplots(figsize=(9.0, 9.0))

ax.plot(
    dev_chart["event_time"], dev_chart["pct_deviation"],
    color=country_color("Mexico"), lw=2.4,
    label="FT’s recipe on the FT’s Mexico series",
)
ax.plot(
    dev_wpp["event_time"], dev_wpp["pct_deviation"],
    color=FT_OXFORD, lw=2.4,
    label="FT’s recipe on UN WPP 2024 (the source the FT uses for the other seven countries)",
)

ax.axhline(0, color=FT_INK, lw=0.7)
ax.axvline(0, color=FT_CLARET, lw=1.4, ls="--")
ax.set_xlabel("Years before / since the FT’s 2013 Mexico take-off")
ax.set_ylabel("% change in TFR vs pre-smartphone trend")
ax.set_xlim(-10, 16)
ax.set_ylim(-42, 7)
ax.legend(loc="lower left", fontsize=11)

fig.subplots_adjust(top=0.84, bottom=0.09, left=0.10, right=0.97)
fig.suptitle(
    "Mexico’s “smartphone shock” disappears under the right data",
    x=0.04, y=0.955, ha="left",
)
fig.text(
    0.04, 0.885,
    "Apply the FT’s recipe to the right data, and the deviation is only −2 per cent.",
    fontsize=13, color="#555555", ha="left",
)
add_source(
    fig,
    "Source: UN WPP 2024; FT Mexico series extracted from the Flourish SVG. "
    "The Catalogue of Errors Ltd.",
)
add_brand(fig)
fig.savefig(FIG / "mexico_chart_vs_wpp.png")
print(f"Wrote {FIG / 'mexico_chart_vs_wpp.png'}")
