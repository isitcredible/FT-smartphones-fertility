"""
Pull Google Trends interest-over-time for 'App Store' / 'Play Store' search
terms in each of the eight FT countries, 2004-2024.

Output: data/google_trends.csv

Note: Google Trends rate-limits aggressively. If a query fails, re-run after
a few minutes. The Trends index is normalised 0-100 per query.
"""
import time
from pathlib import Path

import pandas as pd
from pytrends.request import TrendReq

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

QUERIES = {
    "USA": ("US", ["App Store", "Google Play"]),
    "GBR": ("GB", ["App Store", "Google Play"]),
    "AUS": ("AU", ["App Store", "Google Play"]),
    "MEX": ("MX", ["App Store", "Google Play", "Play Store"]),
    "IDN": ("ID", ["Play Store", "App Store"]),
    "IRN": ("IR", ["Play Store", "App Store"]),
    "EGY": ("EG", ["Play Store", "App Store", "متجر بلاي"]),
    "SEN": ("SN", ["Play Store", "App Store"]),
}

pytrends = TrendReq(hl="en-US", tz=0, timeout=(10, 30))

frames = []
for iso, (geo, terms) in QUERIES.items():
    pytrends.build_payload(
        kw_list=terms, timeframe="2004-01-01 2024-12-31", geo=geo, gprop=""
    )
    df = pytrends.interest_over_time()
    if df.empty:
        print(f"  {iso}: no data")
        continue
    df = df.drop(columns=["isPartial"], errors="ignore").reset_index()
    df["iso3"] = iso
    df = df.melt(id_vars=["date", "iso3"], var_name="term", value_name="interest")
    frames.append(df)
    print(f"  {iso}: {len(df)} rows")
    time.sleep(2)

pd.concat(frames, ignore_index=True).to_csv(DATA / "google_trends.csv", index=False)
print(f"Wrote {DATA / 'google_trends.csv'}")
