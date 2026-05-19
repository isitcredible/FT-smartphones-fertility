"""
Produce the smartphone-ownership-at-take-off table used in the README and
on the isitcredible CASES page.

Take-off years are the years the FT chart actually uses (the chart-implied
years recovered from the saved Flourish SVG), not the ones the article
prose names. The two sets agree for the US, Indonesia and Iran and diverge
for the other five countries; in every case the chart's take-off year is
several years earlier than the year by which Pew's data show smartphones
were widely owned in the country.

Smartphone-ownership figures (% of adults) are taken from Pew Research
Center where available and back-extrapolated from Pew's earliest country
observation where the FT's chart-implied take-off year predates Pew's
country coverage.

Output: data/adoption_table.csv  +  printed markdown table.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

rows = [
    ("United States", 2007, "~0%",
     "iPhone launched mid-2007; Pew's first US observation is 35% in 2011"),
    ("United Kingdom", 2009, "~15%",
     "Pew's first UK observation is 55% in 2013; back-extrapolation from "
     "later Pew rounds gives mid-teens for 2009"),
    ("Australia", 2008, "<10%",
     "ACMA/Deloitte's first observation is 65% in 2013; iPhone 3G launched "
     "mid-2008"),
    ("Mexico", 2013, "21%",
     "Pew 2013 Global Attitudes round (direct observation)"),
    ("Indonesia", 2012, "~10%",
     "Pew 2013: 14%; linear back-extrapolation gives ~10% for 2012"),
    ("Iran", 2015, "~36%",
     "ISPA estimate; consistent with Pew 2014: 25% and Pew 2017: 58%"),
    ("Egypt", 2014, "~22%",
     "Interpolation between Pew 2013: 17% and Pew 2015: 28%"),
    ("Senegal", 2013, "~14%",
     "Pew 2014: 16% and Pew 2015: 19%; back-extrapolation gives ~14%"),
]

cols = ["country", "ft_chart_takeoff_year", "smartphone_ownership_pct", "source"]
df = pd.DataFrame(rows, columns=cols)
df.to_csv(DATA / "adoption_table.csv", index=False)

print("| Country | FT chart take-off year | Smartphone ownership in that year |")
print("|---|---|---|")
for _, r in df.iterrows():
    print(f"| {r['country']} | {r['ft_chart_takeoff_year']} | {r['smartphone_ownership_pct']} |")

print(f"\nWrote {DATA / 'adoption_table.csv'}")
