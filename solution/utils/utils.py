import pandas as pd
import pycountry
import ast
import seaborn as sns
import matplotlib.pyplot as plt
import colorsys

#anime production over time by genre
def parse_genres(x):
    if isinstance(x, list):
        return x
    try:
        return ast.literal_eval(x)
    except:
        return []

#where is the anime community concentrated e Countries with at Least One Person in the Credits

COUNTRY_FIX = {
    "Usa": "United States",
    "US": "United States",
    "United States Of America": "United States",
    "USA": "United States",
    "U.S.A.": "United States",
    "U.S.": "United States",
    "U.K.": "United Kingdom",
    "England": "United Kingdom",
    "Scotland": "United Kingdom",
    "UK": "United Kingdom",
    "England": "United Kingdom",
    "Scotland": "United Kingdom",
    "Russian Federation": "Russia",
    "Korea, Republic of": "South Korea",
    "Korea, Rep.": "South Korea",
    "Turkey": "Türkiye",
    "Turkiye": "Türkiye"
}


def to_iso3(country):
    if pd.isna(country):
        return pd.NA
    try:
        return pycountry.countries.lookup(country).alpha_3
    except:
        return pd.NA

#status
WATCH_STATUS_COLS = ["watching", "completed", "on_hold", "dropped", "plan_to_watch"]

WATCH_STATUS_LABELS = {
    "watching": "Watching",
    "completed": "Completed",
    "on_hold": "On Hold",
    "dropped": "Dropped",
    "plan_to_watch": "Plan to Watch"
}

WATCH_STATUS_ORDER = ["Watching", "Completed", "On Hold", "Dropped", "Plan to Watch"]