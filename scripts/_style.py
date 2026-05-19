"""
FT-inspired matplotlib style for the smartphone-fertility audit figures.

Colours are taken from the saved Flourish embed for John Burn-Murdoch's
chart ("Why birth rates are falling everywhere all at once," Financial Times,
16 May 2026): country lines are #5CC9E0 and regional averages are #0F5499.
Cream background, accent claret and source-line footers follow standard
FT charting practice.

Two palettes are exposed:

  COUNTRY_COLOR — single colour ``#5CC9E0`` used for every country in
                  small-multiples figures (mirroring the FT chart).
  OVERLAY_COLORS — eight distinct hues drawn from the wider FT palette,
                  used when the eight countries are plotted in one panel.
"""
from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt


FT_CREAM = "#FFF1E5"
FT_INK = "#262A33"
FT_CLARET = "#990F3D"
FT_OXFORD = "#0F5499"
FT_CYAN = "#5CC9E0"
FT_GRID = "#D9D2C7"

COUNTRY_COLOR = FT_CYAN

OVERLAY_COLORS = {
    "United States": "#990F3D",   # claret
    "United Kingdom": "#0F5499",  # oxford blue
    "Australia": "#0D7680",       # deep teal
    "Mexico": "#C7A33B",          # mustard
    "Indonesia": "#5CC9E0",       # FT cyan
    "Iran": "#593380",            # aubergine
    "Egypt": "#FF8833",           # orange
    "Senegal": "#4E9F6F",         # forest
}


def apply_ft_style() -> None:
    """Set matplotlib rcParams to an FT-inspired look."""
    mpl.rcParams.update({
        "font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 13,
        "axes.titlesize": 16,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 14,
        "axes.labelsize": 13,
        "axes.labelcolor": FT_INK,
        "axes.edgecolor": FT_INK,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.facecolor": FT_CREAM,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": FT_GRID,
        "grid.linewidth": 0.6,
        "grid.alpha": 0.9,
        "xtick.color": FT_INK,
        "ytick.color": FT_INK,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "figure.facecolor": FT_CREAM,
        "figure.titlesize": 22,
        "figure.titleweight": "bold",
        "legend.frameon": False,
        "legend.fontsize": 12,
        "legend.labelcolor": FT_INK,
        "text.color": FT_INK,
        "savefig.facecolor": FT_CREAM,
        "savefig.edgecolor": FT_CREAM,
        "savefig.dpi": 200,
    })


def country_color(name: str) -> str:
    """Return the overlay-palette colour for a country."""
    return OVERLAY_COLORS.get(name, FT_CYAN)


def add_source(fig, text: str) -> None:
    """Add an italic source/credit line at bottom-left, FT style."""
    fig.text(
        0.01, 0.005, text,
        ha="left", va="bottom",
        fontsize=10, style="italic", color="#666666",
    )


def add_brand(fig) -> None:
    """Add an 'isitcredible.com' brand mark at bottom-right of the figure."""
    fig.text(
        0.99, 0.005, "isitcredible.com",
        ha="right", va="bottom",
        fontsize=11, fontweight="bold", color=FT_CLARET,
    )


def add_subtitle(fig, text: str) -> None:
    """Add a left-aligned subtitle just under the suptitle."""
    fig.text(
        0.01, 0.93, text,
        ha="left", va="top",
        fontsize=13, color="#444444",
    )
