# FT smartphones and fertility — replication data and code

Replication package for the audit of John Burn-Murdoch, "Why Birth
Rates Are Falling Everywhere All at Once," *Financial Times*,
16 May 2026.

For the full write-up, see
[isitcredible.com/cases](https://isitcredible.com/cases).

## Contents

```
data/
  ft_chart_slide0_tfr_by_year.csv         FT chart TFR series by calendar year
  ft_chart_slide3_tfr_eventtime.csv       FT chart TFR series in event time
  ft_chart_slide4_deviation_eventtime.csv FT chart % deviation series in event time
  mexico_chart_vs_wpp.csv                 FT's Mexico TFR series vs UN WPP 2024
  tfr_annual.csv                          UN WPP 2024 TFR, 1950–2023, all countries
  google_trends.csv                       Google Trends interest, 'App Store' / 'Play Store'
  pew_smartphone.csv                      Pew Research Center smartphone ownership
  adoption_table.csv                      Smartphone-ownership-at-take-off summary

scripts/
  _style.py                       Shared FT-inspired matplotlib style
  01_download_tfr.py              UN WPP 2024 → tfr_annual.csv
  02_plot_raw_fertility.py        Raw TFR small multiples
  03_download_google_trends.py    Google Trends pull
  04_plot_google_trends.py        Google Trends small multiples
  05_adoption_table.py            Smartphone-ownership table
  06_replicate_ft_chart.py        Two-panel deviation chart (prose vs chart years)
  07_replicate_chart_implied.py   Single-panel deviation chart (chart years)
  08_pretrend_extrapolation.py    Per-country actual TFR + extrapolated pre-trend
  09_mexico_chart_vs_wpp.py       Mexico FT recipe applied to two data sources

figures/
  *.png                           Output figures used in the write-up
```

## Reproducing

```bash
pip install -r requirements.txt
python scripts/01_download_tfr.py
python scripts/02_plot_raw_fertility.py
python scripts/03_download_google_trends.py
python scripts/04_plot_google_trends.py
python scripts/05_adoption_table.py
python scripts/06_replicate_ft_chart.py
python scripts/07_replicate_chart_implied.py
python scripts/08_pretrend_extrapolation.py
python scripts/09_mexico_chart_vs_wpp.py
```

The UN WPP download is ~16 MB. The Google Trends pull takes about a
minute and is subject to Google's rate limits.

## Sources

- Total fertility rate: UN World Population Prospects 2024, medium
  variant, Country/Area level, observed 1950–2023.
- Google Trends: trends.google.com, country-restricted queries.
- Smartphone ownership: Pew Research Center Global Attitudes Survey,
  Pew Mobile Fact Sheet, ACMA Communications Report, Deloitte Mobile
  Consumer Survey, ISPA / Statista.
- FT chart data and chart-implied take-off years: extracted from the
  rendered Flourish SVG of the FT page saved on 16 May 2026.

## Licence

MIT. Author: Joseph Francis.

Part of [isitcredible.com](https://isitcredible.com), run by The
Catalogue of Errors Ltd.
