import plotly.express as px
from src.utils.common_functions import load_data
from src.utils.athletes_data import medals_per_athlete_by_sport


# histogramme des 10 pays avec le plus de médailles.
def create_top_10_bar_chart():
    #On charge les données
    df = load_data()

    #si le fichier est vide ou introuvable
    if df.empty:
        return {}  # On retourne un graphique vide

    # On compte combien de fois chaque pays apparaît
    df_counts = df['country'].value_counts().reset_index()
    df_counts.columns = ['country', 'count']

    # On garde les 10 premiers
    top_10 = df_counts.head(10)

    #Création du Visuel
    fig = px.bar(
        top_10,
        x='country',
        y='count',
        title="🥇 Top 10 des Nations (Nombre de médailles)",
        color='count',
        labels={'count': 'Nombre de médailles', 'country': 'Pays'}
    )

    return fig

def create_athlete_medals_hist(sport: str, max_medals: int = 10):
    medals = medals_per_athlete_by_sport(sport)

    medals["medal_count_capped"] = medals["medal_count"].clip(upper=max_medals)

    fig = px.histogram(
        medals,
        x="medal_count_capped",
        nbins=max_medals,
        title="Distribution du nombre de médailles par athlète",
        labels={
            "medal_count_capped": f"Nombre de médailles (cap à {max_medals})",
            "count": "Nombre d'athlètes",
        },
    )
    fig.update_layout(bargap=0.1)
    return fig