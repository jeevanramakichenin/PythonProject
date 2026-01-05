from dash import html, dcc, dash_table
from src.components.figures import create_top_10_bar_chart
from src.utils.map_folium import build_medals_map_html
from src.utils.athletes_data import get_sports_list

sports = get_sports_list()

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

    #La map folium
    html.Div([
        html.H3("Carte : % de médailles (Or / Argent / Bronze) pour un pays"),
        html.P("Cette carte choroplèthe représente la proportion de médailles d’or/argent/bronze parmi l’ensemble des médailles obtenues par chaque pays aux Jeux Olympiques d’été."),
        html.Iframe(
            srcDoc=build_medals_map_html(),
            style={"width": "100%", "height": "650px", "border": "none"}
        )
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px'}),

    #Slider athlete par medaille
    #(Sport dropdown + slider + histogramme + aperçu)
    html.Div([
        html.H3("Athlètes : distribution du nombre de médailles"),
        html.P(
            "Filtre par sport puis explore la distribution des athlètes selon leur nombre de médailles.",
            style={'padding': '20px',"marginTop": "6px", "color": "#666", "fontSize": "14px"}
        ),

        html.Div([
            html.Label("Sport"),
            dcc.Dropdown(
                id="sport-dropdown",
                options=[{"label": "Tous les sports", "value": "ALL"}]
                        + [{"label": s, "value": s} for s in sports],
                value="ALL",
                clearable=False,
            ),
        ], style={"marginBottom": "12px"}),

        html.Div([
            html.Label("Cap max médailles (pour lisibilité)"),
            dcc.Slider(
                id="max-medals-slider",
                min=3, max=30, step=1, value=10,
                marks={i: str(i) for i in [3,5,10,15,20,25,30]},
            ),
        ], style={"marginBottom": "12px"}),

        dcc.Graph(id="athlete-hist"),

        html.H4("Aperçu des athlètes (Top 20)"),
        dash_table.DataTable(
            id="athlete-table",
            columns=[
                {"name": "Athlète", "id": "athlete"},
                {"name": "Nombre de médailles", "id": "medal_count"},
            ],
            data=[],
            page_size=20,
            sort_action="native",
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "6px"},
            style_header={"fontWeight": "bold"},
        ),
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px'}),


    
])