"""
Download UN World Population Prospects 2024 demographic indicators and extract
the annual total fertility rate (TFR) series for every country, 1950-2023.

Output: data/tfr_annual.csv
"""
import gzip
import shutil
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

URL = (
    "https://population.un.org/wpp/assets/Excel%20Files/"
    "1_Indicator%20(Standard)/CSV_FILES/"
    "WPP2024_Demographic_Indicators_Medium.csv.gz"
)
GZ_PATH = DATA / "wpp_demographic_indicators.csv.gz"
CSV_PATH = DATA / "wpp_demographic_indicators.csv"

if not CSV_PATH.exists():
    if not GZ_PATH.exists():
        print(f"Downloading {URL} ...")
        urllib.request.urlretrieve(URL, GZ_PATH)
    with gzip.open(GZ_PATH, "rb") as f_in, open(CSV_PATH, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

cols = ["ISO3_code", "LocTypeName", "Location", "Time", "TFR"]
df = pd.read_csv(CSV_PATH, usecols=cols, low_memory=False)
df = df[df["LocTypeName"] == "Country/Area"]
df = df[df["Time"] <= 2023]
df = df[["ISO3_code", "Location", "Time", "TFR"]].rename(
    columns={"Time": "year", "ISO3_code": "iso3", "Location": "country"}
)
df.to_csv(DATA / "tfr_annual.csv", index=False)
print(f"Wrote {len(df):,} country-year rows for {df['iso3'].nunique()} countries")
