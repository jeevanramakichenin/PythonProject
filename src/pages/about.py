from dash import html

layout = html.Div([
    html.H1("À Propos du Projet", style={'textAlign': 'center'}),

    html.Div([
        html.H3("L'Équipe"),
        html.P("Ce dashboard a été réalisé par :"),
        html.Ul([
            html.Li("Jeevan RAMAKICHENIN"),
            html.Li("Ilo RABIARIVELO")
        ]),

        html.Hr(),

        html.H3("Les Données"),
        html.P("Nous utilisons le dataset historique des Jeux Olympiques (120 ans d'histoire)."),
        html.P("Source : Kaggle / Rgriffin"),

        html.Hr(),

        html.H3("Objectif"),
        html.P("Visualiser les tendances géopolitiques à travers les médailles olympiques.")
    ], style={'padding': '20px', 'maxWidth': '800px', 'margin': '0 auto'})
])