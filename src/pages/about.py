from dash import html
import dash_bootstrap_components as dbc

NAVY_BLUE = "#2c3e50"
GOLD = "#d4af37"
CARD_HEADER_STYLE = {"backgroundColor": GOLD, "color": NAVY_BLUE, "fontWeight": "bold"}

layout = dbc.Container([

    dbc.Row([
        dbc.Col([

            dbc.Card([
                dbc.CardHeader("👥 L'Équipe", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Ce dashboard a été réalisé par :", className="mb-2"),
                    html.Ul([
                        html.Li("Jeevan RAMAKICHENIN", className="fw-bold"),
                        html.Li("Ilo RABIARIVELO", className="fw-bold")
                    ], className="mb-0")
                ], className="p-3")
            ], className="shadow-sm mb-4"),

            dbc.Card([
                dbc.CardHeader("📊 Les Données", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Dataset historique des Jeux Olympiques d'été (1896-2012).", className="mb-2"),
                    html.P([
                        html.Strong("Source : "),
                        html.A("Kaggle - Olympic Games Dataset", href="https://www.kaggle.com/datasets/the-guardian/olympic-games", target="_blank", style={"color": NAVY_BLUE})
                    ], className="mb-0")
                ], className="p-3")
            ], className="shadow-sm mb-4"),

            dbc.Card([
                dbc.CardHeader("🎯 Objectif", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Visualiser les tendances historiques et géopolitiques à travers l'analyse des médailles olympiques.", className="mb-2"),
                    html.P("Explorer l'évolution de la parité homme/femme et la domination des nations.", className="mb-0 text-muted")
                ], className="p-3")
            ], className="shadow-sm mb-4"),

            dbc.Card([
                dbc.CardHeader("🛠️ Technologies", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Ce dashboard a été développé avec :", className="mb-2"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Badge("Python", style={"backgroundColor": NAVY_BLUE}, className="me-2 mb-2"),
                            dbc.Badge("Dash", style={"backgroundColor": NAVY_BLUE}, className="me-2 mb-2"),
                            dbc.Badge("Plotly", style={"backgroundColor": NAVY_BLUE}, className="me-2 mb-2"),
                            dbc.Badge("Pandas", style={"backgroundColor": GOLD, "color": NAVY_BLUE}, className="me-2 mb-2"),
                            dbc.Badge("Folium", style={"backgroundColor": NAVY_BLUE}, className="me-2 mb-2"),
                            dbc.Badge("Bootstrap", style={"backgroundColor": NAVY_BLUE}, className="me-2 mb-2"),
                        ])
                    ])
                ], className="p-3")
            ], className="shadow-sm mb-4"),

        ], lg=8, md=10, sm=12, className="mx-auto")
    ]),

], style={"maxWidth": "1200px", "margin": "0 auto", "padding": "0 20px"}, className="bg-light")