from dash import html, dcc
from src.components.figures import create_top_10_bar_chart

#On setup le Layout
layout = html.Div([
    html.H1("Dashboard Jeux Olympiques", style={'textAlign': 'center', 'marginBottom': '20px'}),
    html.P("Bienvenue sur l'outil d'analyse des médailles olympiques", style={'textAlign': 'center'}),

    html.Hr(),

    #le conteneur du graphique
    html.Div([
        html.H3("Répartition des médailles par pays"),
        dcc.Graph(figure=create_top_10_bar_chart())
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px'})
])