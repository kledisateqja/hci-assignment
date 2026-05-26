import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import plotly.graph_objects as go


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
# Aggiunge una traccia per ogni fascia di punteggio con area colorata e stile personalizzato
def add_score_band_traces(fig, matrix_melted, band_counts, palette):
    for band, color in palette.items():
        df_band = matrix_melted[matrix_melted["score_band"] == band]
        n = band_counts.get(band, 0)
        fig.add_trace(go.Scatter(
            x=df_band["voto"],
            y=df_band["percentuale"],
            mode="lines+markers",
            name=f"{band}  ({n:,} anime)",
            line=dict(color=color, width=3),
            marker=dict(size=8, color=color, line=dict(color="white", width=1.5)),
            fill="tozeroy",
            fillcolor=color.replace("#", "rgba(").replace("e74c3c", "231,76,60,0.12)")
                           .replace("f39c12", "243,156,18,0.12)")
                           .replace("2ecc71", "46,204,113,0.12)"),
            hovertemplate="<b>%{fullData.name}</b><br>Voto: %{x}<br>% utenti: %{y:.1f}%<extra></extra>"
        ))
    return fig

# Disegna il gauge semicircolare con ago e testo per il rating medio
def draw_gauge(ax, avg_user_rating, fav_count):
    theta = np.linspace(0, np.pi, 300)
    ax.plot(np.cos(theta), np.sin(theta), color='lightgray', lw=20, solid_capstyle='round')

    for start, end, color in [
        (0,    0.5,  '#32cd3250'),
        (0.5,  0.75, '#ffa50050'),
        (0.75, 1.0,  '#ff634750')
    ]:
        t = np.linspace(start * np.pi, end * np.pi, 100)
        ax.plot(np.cos(t), np.sin(t), lw=18, color=color, solid_capstyle='butt')

    angle = np.pi * (1 - avg_user_rating / 10)
    ax.annotate('', xy=(0.6 * np.cos(angle), 0.6 * np.sin(angle)), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='steelblue', lw=3))
    ax.text(0, -0.2,  f'{avg_user_rating:.2f}/10', ha='center', fontsize=22, fontweight='bold')
    ax.text(0, -0.45, f'Preferiti: {fav_count:,}', ha='center', fontsize=11, color='gray')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.6, 1.2)
    ax.axis('off')
    ax.set_title('Rating medio', fontsize=13)


# Applica i colori e lo stile alle parti del violin plot
def style_violin(parts):
    parts['bodies'][0].set_facecolor('steelblue')
    parts['bodies'][0].set_alpha(0.7)
    parts['cmedians'].set_color('white')
    parts['cbars'].set_color('navy')
    parts['cmins'].set_color('navy')
    parts['cmaxes'].set_color('navy')

# Aggiunge le linee verticali del lollipop chart per ogni lingua
def add_lollipop_lines(fig, lang_stats):
    for _, row in lang_stats.iterrows():
        fig.add_shape(
            type="line",
            x0=row["language"], x1=row["language"],
            y0=0, y1=row["anime_count"],
            line=dict(color="#9b59b6", width=2)
        )
    return fig

# Aggiunge le etichette in milioni a destra di ogni barra orizzontale
def label_horizontal_bars(bars, totals):
    for bar, val in zip(bars, totals):
        plt.text(
            bar.get_width() + totals.max() * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{val / 1_000_000:.2f}M", va="center", fontsize=10
        )


# Applica lo stile bianco grassetto alle percentuali del pie chart dei personaggi
def style_character_autotexts(autotexts):
    for t in autotexts:
        t.set_color("white")
        t.set_fontweight("bold")


# Aggiunge le etichette percentuali sopra ogni barra del bar chart
def label_bars(bars, totals):
    for bar, val in zip(bars, totals):
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.1f}%", ha="center", fontsize=10)