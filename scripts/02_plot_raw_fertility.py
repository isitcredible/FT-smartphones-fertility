"""
Plot raw TFR series, 1990-2023, for each of Burn-Murdoch's eight countries,
in two parallel panels: one annotated with the take-off year the FT article
prose states, and one with the take-off year the chart actually uses.

Output: figures/raw_fertility_rates.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from _style import (
    FT_CLARET, FT_OXFORD, COUNTRY_COLOR,
    add_source, apply_ft_style,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

# (iso3, country name, prose take-off year, chart-implied take-off year)
# Chronological by chart-implied take-off; alphabetical within year.
COUNTRIES = [
    ("USA", "United States",  2007, 2007),
    ("AUS", "Australia",      2007, 2008),
    ("GBR", "United Kingdom", 2007, 2009),
    ("IDN", "Indonesia",      2012, 2012),
    ("MEX", "Mexico",         2012, 2013),
    ("SEN", "Senegal",        2015, 2013),
    ("EGY", "Egypt",          2015, 2014),
    ("IRN", "Iran",           2015, 2015),
]

apply_ft_style()
tfr = pd.read_csv(DATA / "tfr_annual.csv")

fig, axes = plt.subplots(2, 4, figsize=(15, 8), sharex=True)
for ax, (iso, name, prose, chart) in zip(axes.flatten(), COUNTRIES):
    s = tfr[tfr["iso3"] == iso].set_index("year")["TFR"].loc[1990:2023]
    ax.plot(s.index, s.values, color=COUNTRY_COLOR, lw=2.2)
    ax.axvline(prose, color=FT_CLARET, lw=1.2, ls="--",
               label=f"Article prose: {prose}")
    if chart != prose:
        ax.axvline(chart, color=FT_OXFORD, lw=1.2, ls=":",
                   label=f"Chart implied: {chart}")
    ax.set_title(name)
    ax.set_xlim(1990, 2023)
    ax.legend(loc="lower left", fontsize=8)

fig.suptitle("Raw total fertility rate, 1990–2023",
             x=0.01, ha="left")
fig.text(0.01, 0.93,
         "FT prose names one set of take-off years; the chart uses another. "
         "Each red dash marks the prose year, each blue dot the year implied by the chart.",
         fontsize=10, color="#555555", ha="left")
fig.supylabel("Births per woman", x=0.005, fontsize=10)
add_source(
    fig,
    "Source: UN World Population Prospects 2024. "
    "Chart-implied take-off years reverse-engineered from FT Flourish SVGs. "
    "isitcredible.com",
)
fig.tight_layout(rect=(0.01, 0.03, 1, 0.92))
fig.savefig(FIG / "raw_fertility_rates.png")
print(f"Wrote {FIG / 'raw_fertility_rates.png'}")
