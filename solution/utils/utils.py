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
# funzione per conertire in stringa
def parse_list_column(x):

        if isinstance(x, list):
            return x
        try:
            return ast.literal_eval(x)
        except:
            return []

# Calcola la media pesata del punteggio per anno con media mobile a 5 anni
def compute_year_weighted(df_weighted):
    year_weighted = df_weighted.groupby('year', group_keys=False).apply(
        lambda x: pd.Series({
            'weighted_mean': (x['score'] * x['scored_by']).sum() / x['scored_by'].sum(),
            'total_votes': x['scored_by'].sum(),
            'anime_count': len(x)
        }),
        include_groups=False).reset_index()
    year_weighted = year_weighted.sort_values('year')
    year_weighted['rolling_weighted'] = year_weighted['weighted_mean'].rolling(
        window=5, center=True, min_periods=2).mean()
    return year_weighted


# Calcola la percentuale di produzione e preferenze fan per genere, restituisce formato long per plotly
def compute_genre_compare(genres_df, favs):
    production = genres_df['genres'].value_counts()
    production_pct = production / production.sum() * 100

    favs_genres = pd.merge(favs, genres_df[['mal_id', 'genres']], on='mal_id', how='inner')
    favs_count = favs_genres['genres'].value_counts()
    favs_pct = favs_count / favs_count.sum() * 100

    compare = pd.DataFrame({'Produzione': production_pct,
                            'Preferenze fan': favs_pct}).dropna()
    compare = compare.sort_values('Produzione', ascending=False)

    compare_long = (compare.rename_axis('Genere').reset_index()
                    .melt(id_vars='Genere', var_name='Tipo', value_name='Percentuale'))
    return compare_long


# Conta gli anime per ogni combinazione anno+tipo, riempie i vuoti con 0 per il grafico animato
def compute_anime_type_counts(details, main_types):
    counts = (details.groupby(['year', 'type']).size().reset_index(name='count'))
    all_combinations = pd.MultiIndex.from_product(
        [counts['year'].unique(), main_types], names=['year', 'type'])
    counts = (counts.set_index(['year', 'type'])
                    .reindex(all_combinations, fill_value=0)
                    .reset_index())
    counts = counts.sort_values(['year', 'type'])
    return counts

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