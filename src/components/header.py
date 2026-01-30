from dash import html
import dash_bootstrap_components as dbc

NAVY_BLUE = "#2c3e50"


def create_header():
    """En-tête commun à toutes les pages."""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("🏅 Dashboard Jeux Olympiques", className="text-center mt-4 mb-2", style={"color": NAVY_BLUE}),
                html.P("Explorez l'histoire des médailles olympiques d'été de 1896 à 2012", className="text-center text-muted mb-4"),
                html.Hr(className="mb-4"),
            ], width=12)
        ]),
    ], fluid=True)
