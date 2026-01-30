from dash import Input, Output
from src.app import app
from src.components.figures import create_athlete_medals_hist, create_top_10_bar_chart, create_evolution_chart
from src.utils.athletes_data import medals_per_athlete_by_sport


def register_callbacks():
    """Enregistre tous les callbacks de l'application."""

    @app.callback(
        Output("top10-chart", "figure"),
        Input("year-dropdown", "value"),
    )
    def update_top10(year):
        return create_top_10_bar_chart(year=year)

    @app.callback(
        Output("evolution-chart", "figure"),
        Input("evolution-sport-dropdown", "value"),
    )
    def update_evolution(sport):
        return create_evolution_chart(sport=sport)

    @app.callback(
        Output("athlete-hist", "figure"),
        Output("athlete-table", "data"),
        Input("sport-dropdown", "value"),
        Input("max-medals-slider", "value"),
    )
    def update_athlete_views(sport, max_medals):
        fig = create_athlete_medals_hist(sport, max_medals=max_medals)
        medals = medals_per_athlete_by_sport(sport)
        top20 = medals.head(20).to_dict("records")
        return fig, top20
