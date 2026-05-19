"""
Replicate the FT's headline % deviation chart using the chart's own data,
not a recomputation. Series are extracted from the saved Flourish
scrollytelling SVG (slide 4) and stored as
``data/ft_chart_slide4_deviation_eventtime.csv``.

Output: figures/replication_chart_implied.png  (square; eye-catching).
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from _style import FT_CLARET, FT_INK, add_brand, add_source, apply_ft_style, country_color

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

ISO_TO_NAME = {
    "USA": "United States",
    "GBR": "United Kingdom",
    "AUS": "Australia",
    "MEX": "Mexico",
    "IDN": "Indonesia",
    "IRN": "Iran",
    "EGY": "Egypt",
    "SEN": "Senegal",
}
# Chronological by chart-implied take-off; alphabetical within year.
ORDER = ["USA", "AUS", "GBR", "IDN", "MEX", "SEN", "EGY", "IRN"]

apply_ft_style()
df = pd.read_csv(DATA / "ft_chart_slide4_deviation_eventtime.csv")

fig, ax = plt.subplots(figsize=(9.0, 9.0))
for iso in ORDER:
    sub = df[df["iso3"] == iso].sort_values("event_time")
    name = ISO_TO_NAME[iso]
    ax.plot(
        sub["event_time"], sub["pct_deviation"],
        color=country_color(name), lw=2.4, label=name,
    )

ax.axhline(0, color=FT_INK, lw=0.7)
ax.axvline(0, color=FT_CLARET, lw=1.4, ls="--")
ax.set_xlabel("Years before / since ‘smartphone take-off’")
ax.set_ylabel("% change in TFR vs pre-smartphone trend")
ax.set_xlim(-10, 16)
ax.set_ylim(-42, 7)
ax.legend(loc="lower left", fontsize=12, ncol=2)

fig.subplots_adjust(top=0.84, bottom=0.09, left=0.10, right=0.97)
fig.suptitle(
    "A replication of the FT’s smartphones-and-fertility chart",
    x=0.04, y=0.955, ha="left",
)
fig.text(
    0.04, 0.885,
    "The underlying data have been extracted from ft.com.",
    fontsize=13, color="#555555", ha="left",
)
add_source(
    fig,
    "Source: data extracted from the saved FT scrollytelling SVG "
    "(axis-calibrated point coordinates). The Catalogue of Errors Ltd.",
)
add_brand(fig)
fig.savefig(FIG / "replication_chart_implied.png")
print(f"Wrote {FIG / 'replication_chart_implied.png'}")
