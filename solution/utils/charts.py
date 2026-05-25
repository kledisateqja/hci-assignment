import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import ast
import plotly.express as px

# Prepara i dati per il pie chart: top N generi + aggregazione "Other"
def get_pie_data(genre_total, top_n=12):
    top_genres_pie = genre_total.head(top_n)
    other_count = genre_total.iloc[top_n:].sum()
    if other_count > 0:
        return pd.concat([top_genres_pie, pd.Series({'Other': other_count})])
    return top_genres_pie


# Calcola l'explode per il pie chart: distacca la fetta con più occorrenze
def get_explode(pie_data):
    return [0.08 if genre == pie_data.idxmax() else 0 for genre in pie_data.index]


# Applica lo stile bianco grassetto alle percentuali del pie chart
def style_autotexts(autotexts):
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')


# Aggiunge una trace per ogni genere al grafico lineare, mostra solo il genere di default
def add_genre_traces(fig, genre_year, default_genre="Action"):
    for genre in sorted(genre_year['genres'].unique()):
        df_g = genre_year[genre_year['genres'] == genre]
        fig.add_trace(
            go.Scatter(
                x=df_g['year'],
                y=df_g['count'],
                mode='lines',
                name=genre,
                visible=True if genre == default_genre else "legendonly",
                line=dict(width=2.5)
            )
        )
    return fig