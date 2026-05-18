"""
Produce the smartphone-ownership-at-take-off table used in the README.

Smartphone ownership figures (% of adults) are hand-keyed from public sources:
  - United States: Pew Research Center, 'Mobile Fact Sheet' (annual trend);
    first measurement 35% in 2011. iPhone launched in mid-2007, so ownership
    in 2007 was effectively zero.
  - United Kingdom, Mexico, Indonesia, Egypt: Pew Research Center, Global
    Attitudes Survey ('Smartphone Ownership Is Growing Rapidly Around the
    World', Feb 2019).
  - Australia: ACMA Communications Report / Deloitte Mobile Consumer Survey.
  - Iran: ISPA / Statista country reports.
  - Senegal: Pew Spring 2017 / 2018 Global Attitudes data points.

For 2007 (US/UK/Australia), Pew's first cross-country smartphone-ownership
observation post-dates the year by several years; the FT take-off year falls
before any survey-measured adoption existed.

Output: data/adoption_table.csv  +  printed markdown table.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

rows = [
    ("United States", 2007, "~0%",
     "iPhone launched mid-2007; Pew's first observation is 35% in 2011"),
    ("United Kingdom", 2007, "~0%",
     "Pew's first UK observation is 55% in 2013"),
    ("Australia", 2007, "~0%",
     "ACMA/Deloitte's first observation is 65% in 2013"),
    ("Mexico", 2012, "~10-15%",
     "Pew 2013: 21%; linear back-extrapolation gives ~12% for 2012"),
    ("Indonesia", 2012, "~10%",
     "Pew 2013: 14%; linear back-extrapolation gives ~10% for 2012"),
    ("Iran", 2015, "~36%",
     "ISPA estimate, broadly consistent with later Pew rounds"),
    ("Egypt", 2015, "~28%",
     "Pew 2015 Global Attitudes round"),
    ("Senegal", 2015, "~19%",
     "Pew 2015 Global Attitudes round"),
]

cols = ["country", "ft_takeoff_year", "smartphone_ownership_pct", "source"]
df = pd.DataFrame(rows, columns=cols)
df.to_csv(DATA / "adoption_table.csv", index=False)

print("| Country | FT take-off year | Smartphone ownership in that year |")
print("|---|---|---|")
for _, r in df.iterrows():
    print(f"| {r['country']} | {r['ft_takeoff_year']} | {r['smartphone_ownership_pct']} |")

print(f"\nWrote {DATA / 'adoption_table.csv'}")
