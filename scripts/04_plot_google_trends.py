"""
Plot Google Trends 'App Store' / 'Play Store' interest-over-time for each of
the eight FT countries, with the FT-stated 'smartphone take-off' year marked.

Output: figures/google_trends.png
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

gt = pd.read_csv(DATA / "google_trends.csv", parse_dates=["date"])
gt["year"] = gt["date"].dt.year

# Take max across search terms per country-month, then mean across months -> annual
agg = gt.groupby(["iso3", "date"])["interest"].max().reset_index()
agg["year"] = agg["date"].dt.year
annual = agg.groupby(["iso3", "year"])["interest"].mean().reset_index()

fig, axes = plt.subplots(2, 4, figsize=(15, 7.5), sharex=True, sharey=True)
fig.suptitle(
    "Google Trends interest in 'App Store' / 'Play Store' "
    "(annual mean of monthly index, max over local-language terms)\n"
    "Red dashed line = FT-stated 'smartphone take-off' year",
    fontsize=11,
)

for ax, (iso, (name, t)) in zip(axes.flatten(), FT.items()):
    sub = annual[annual["iso3"] == iso].sort_values("year")
    ax.plot(sub["year"], sub["interest"], color="steelblue", lw=1.6)
    ax.axvline(t, color="red", lw=1.2, ls=":")
    v = sub.set_index("year")["interest"].get(t)
    if pd.notna(v):
        ax.scatter([t], [v], color="red", s=60, zorder=5)
        ax.annotate(
            f"{int(round(v))} / 100",
            xy=(t, v),
            xytext=(t + 0.5, v + 5),
            fontsize=10,
            color="red",
        )
    ax.set_title(f"{name} (FT take-off {t})")
    ax.grid(alpha=0.3)
    ax.set_xlim(2004, 2024)
    ax.set_ylim(0, 100)

fig.supylabel("Google Trends index (0-100, country-relative)")
fig.supxlabel("Year")
fig.tight_layout()
fig.savefig(FIG / "google_trends.png", dpi=160)
print(f"Wrote {FIG / 'google_trends.png'}")
