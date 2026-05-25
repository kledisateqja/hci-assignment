import pandas as pd
import pycountry
import ast

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

# Calcola la matrice delle distribuzioni percentuali di voto per fascia di punteggio
def compute_score_band_matrix(details, df_stats):
    score_cols = df_stats.filter(regex=r"^score_\d+_votes$").columns.tolist()
    loved = (details.merge(df_stats[["mal_id"] + score_cols], on="mal_id")
                    .dropna(subset=["score"] + score_cols))
    loved["score_band"] = pd.cut(loved["score"], bins=[1, 6, 8, 10],
                                 labels=["Basso (1–6)", "Medio (6–8)", "Alto (8–10)"])
    band_counts = loved["score_band"].value_counts()
    loved_pct = loved[score_cols].div(loved[score_cols].sum(axis=1), axis=0) * 100
    loved_pct["score_band"] = loved["score_band"].values
    matrix = loved_pct.groupby("score_band", observed=True)[score_cols].mean().reset_index()
    matrix_melted = matrix.melt(id_vars="score_band", var_name="voto", value_name="percentuale")
    matrix_melted["voto"] = matrix_melted["voto"].str.split("_").str[1].astype(int)
    return matrix_melted, band_counts

# Calcola il voto medio per fascia di raccomandazioni ricevute
def compute_rec_score_summary(data):
    bins = [0, 5, 20, 50, float('inf')]
    tier_labels = ['1–5', '6–20', '21–50', '51+']
    data['rec_tier'] = pd.cut(data['n_recs'], bins=bins, labels=tier_labels)
    summary = (data.groupby('rec_tier', observed=True)['avg_score']
                   .agg(media='mean', n_anime='count')
                   .reset_index())
    summary['etichetta'] = summary.apply(
        lambda r: f"{r['media']:.2f} ({int(r['n_anime'])} anime)", axis=1)
    return summary

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