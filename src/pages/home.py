from dash import html, dcc
from src.components.figures import create_top_10_bar_chart
from src.utils.map_folium import build_medals_map_html


#On setup le Layout
layout = html.Div([
    html.H1("Dashboard Jeux Olympiques", style={'textAlign': 'center', 'marginBottom': '20px'}),
    html.P("Bienvenue sur l'outil d'analyse des médailles olympiques", style={'textAlign': 'center'}),

    html.Hr(),

    #le conteneur du graphique
    html.Div([
        html.H3("Répartition des médailles par pays"),
        dcc.Graph(figure=create_top_10_bar_chart())
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px'}),

    html.Br(),

    #la map folium
    html.Div([
        html.H3("Carte : % de médailles (Or / Argent / Bronze)"),
        html.Iframe(
            srcDoc=build_medals_map_html(),
            style={"width": "100%", "height": "650px", "border": "none"}
        )
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px'})


    
])