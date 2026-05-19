"""
Plot Google Trends 'App Store' / 'Play Store' interest-over-time for each of
the eight FT countries, with the FT-stated 'smartphone take-off' year marked.

Output: figures/google_trends.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from _style import (
    FT_CLARET, FT_OXFORD, COUNTRY_COLOR,
    add_brand, add_source, apply_ft_style,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

# Chart-implied take-off years (chronological, alphabetical within year).
COUNTRIES = [
    ("USA", "United States",  2007),
    ("AUS", "Australia",      2008),
    ("GBR", "United Kingdom", 2009),
    ("IDN", "Indonesia",      2012),
    ("MEX", "Mexico",         2013),
    ("SEN", "Senegal",        2013),
    ("EGY", "Egypt",          2014),
    ("IRN", "Iran",           2015),
]

apply_ft_style()
gt = pd.read_csv(DATA / "google_trends.csv", parse_dates=["date"])
gt["year"] = gt["date"].dt.year

agg = gt.groupby(["iso3", "date"])["interest"].max().reset_index()
agg["year"] = agg["date"].dt.year
annual = agg.groupby(["iso3", "year"])["interest"].mean().reset_index()

fig, axes = plt.subplots(2, 4, figsize=(15, 8), sharex=True, sharey=True)
for ax, (iso, name, takeoff) in zip(axes.flatten(), COUNTRIES):
    sub = annual[annual["iso3"] == iso].sort_values("year")
    ax.plot(sub["year"], sub["interest"], color=COUNTRY_COLOR, lw=2.2)
    ax.axvline(takeoff, color=FT_CLARET, lw=1.4, ls="--")
    v = sub.set_index("year")["interest"].get(takeoff)
    if pd.notna(v):
        ax.scatter([takeoff], [v], color=FT_CLARET, s=45, zorder=5)
        ax.annotate(
            f"{takeoff} ({int(round(v))}%)",
            xy=(takeoff, v),
            xytext=(takeoff + 0.6, max(v + 6, 8)),
            fontsize=11, color=FT_CLARET,
        )
    ax.set_title(name)
    ax.set_xlim(2004, 2024)
    ax.set_ylim(0, 100)

fig.subplots_adjust(top=0.82, bottom=0.07, left=0.05, right=0.99, hspace=0.30, wspace=0.18)
fig.suptitle("Google Trends interest in ‘App Store’ / ‘Play Store’ / ‘Android Market’",
             x=0.01, y=0.965, ha="left")
fig.text(0.01, 0.905,
         "Annual mean of the monthly index, max over local-language terms "
         "(‘Android Market’ being Google Play’s name before March 2012). "
         "Index is 0–100 relative to each country’s own peak.",
         fontsize=12, color="#555555", ha="left")
fig.supylabel("Index (country-relative, 0–100)", x=0.005, fontsize=12)
add_source(
    fig,
    "Source: Google Trends. The Catalogue of Errors Ltd.",
)
add_brand(fig)
fig.savefig(FIG / "google_trends.png")
print(f"Wrote {FIG / 'google_trends.png'}")
