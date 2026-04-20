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

