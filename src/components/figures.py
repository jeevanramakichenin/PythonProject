import plotly.express as px
import plotly.io as pio
from src.utils.common_functions import load_data
from src.utils.athletes_data import medals_per_athlete_by_sport

pio.templates.default = "plotly_white"

# Palette de couleurs
NAVY_BLUE = "#2c3e50"
GOLD = "#d4af37"
LIGHT_GOLD = "#f4e4ba"


def create_top_10_bar_chart(year=None):
    """Histogramme des 10 pays avec le plus de médailles."""
    df = load_data()
    if df.empty:
        return {}

    if year and year != "ALL":
        df = df[df['year'] == int(year)]

    df_counts = df['country'].value_counts().reset_index()
    df_counts.columns = ['country', 'count']
    top_10 = df_counts.head(10)

    fig = px.bar(
        top_10, x='country', y='count',
        color='count',
        color_continuous_scale=[[0, LIGHT_GOLD], [1, GOLD]],
        labels={'count': 'Médailles', 'country': 'Pays'}
    )
    fig.update_layout(
        showlegend=False, coloraxis_showscale=False,
        font_color=NAVY_BLUE,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_traces(marker_line_color=NAVY_BLUE, marker_line_width=1)
    return fig


def create_athlete_medals_hist(sport: str, max_medals: int = 10):
    """Histogramme de la distribution des médailles par athlète."""
    medals = medals_per_athlete_by_sport(sport)
    medals["medal_count_capped"] = medals["medal_count"].clip(upper=max_medals)

    fig = px.histogram(
        medals, x="medal_count_capped", nbins=max_medals,
        labels={"medal_count_capped": f"Médailles (max {max_medals})", "count": "Athlètes"},
        color_discrete_sequence=[GOLD]
    )
    fig.update_layout(
        bargap=0.1, font_color=NAVY_BLUE,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_traces(marker_line_color=NAVY_BLUE, marker_line_width=1)
    return fig


def create_evolution_chart(sport="ALL"):
    """Graphique de l'évolution des médailles par genre."""
    df = load_data()
    if df.empty:
        return {}

    if sport and sport != "ALL":
        df = df[df['sport'] == sport]

    evolution = df.groupby(['year', 'gender']).size().reset_index(name='count')

    fig = px.line(
        evolution, x='year', y='count', color='gender', markers=True,
        labels={'year': 'Année', 'count': 'Médailles', 'gender': 'Genre'},
        color_discrete_map={'Men': NAVY_BLUE, 'Women': GOLD}
    )
    fig.update_layout(
        legend_title_text='Genre', hovermode='x unified',
        font_color=NAVY_BLUE,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_traces(line_width=3)
    return fig