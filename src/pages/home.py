from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from src.utils.map_folium import build_medals_map_html
from src.utils.athletes_data import get_sports_list, get_years_list

sports = get_sports_list()
years = get_years_list()

NAVY_BLUE = "#2c3e50"
GOLD = "#d4af37"
CARD_HEADER_STYLE = {"backgroundColor": GOLD, "color": NAVY_BLUE, "fontWeight": "bold"}

layout = dbc.Container([

    # Section 1 : Top 10 + Évolution
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📊 Top 10 des Nations", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    dbc.Label("Édition", className="fw-bold small"),
                    dcc.Dropdown(
                        id="year-dropdown",
                        options=[{"label": "🏆 Toutes les éditions", "value": "ALL"}]
                                + [{"label": f"{int(y)}", "value": str(int(y))} for y in years],
                        value="ALL", clearable=False, style={"marginBottom": "10px"}
                    ),
                    dcc.Graph(id="top10-chart", style={"height": "320px"}, config={"displayModeBar": False})
                ], className="p-3")
            ], className="shadow-sm h-100")
        ], lg=6, md=12, className="mb-4"),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📈 Évolution par Genre", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    dbc.Label("Sport", className="fw-bold small"),
                    dcc.Dropdown(
                        id="evolution-sport-dropdown",
                        options=[{"label": "Tous les sports", "value": "ALL"}]
                                + [{"label": s, "value": s} for s in sports],
                        value="ALL", clearable=False, style={"marginBottom": "10px"}
                    ),
                    dcc.Graph(id="evolution-chart", style={"height": "320px"}, config={"displayModeBar": False})
                ], className="p-3")
            ], className="shadow-sm h-100")
        ], lg=6, md=12, className="mb-4"),
    ], className="g-4"),

    # Section 2 : Carte
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🗺️ Répartition Géographique des Médailles", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Proportion de médailles d'or, d'argent et de bronze par pays.", className="text-muted small mb-3"),
                    html.Iframe(srcDoc=build_medals_map_html(), style={"width": "100%", "height": "500px", "border": "none", "borderRadius": "8px"})
                ], className="p-3")
            ], className="shadow-sm")
        ], lg=12, className="mb-4"),
    ]),

    # Section 3 : Athlètes
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🏆 Aperçu des Athlètes (Top 20)", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Les athlètes les plus médaillés.", className="text-muted small mb-3"),
                    dash_table.DataTable(
                        id="athlete-table",
                        columns=[{"name": "Athlète", "id": "athlete"}, {"name": "Médailles", "id": "medal_count"}],
                        data=[],
                        page_size=10,
                        sort_action="native",
                        cell_selectable=False,
                        style_table={"overflowX": "auto"},
                        style_cell={"textAlign": "left", "padding": "8px 12px", "fontSize": "14px"},
                        style_header={"fontWeight": "bold", "backgroundColor": "#f8f9fa", "borderBottom": f"2px solid {GOLD}"},
                        style_data_conditional=[
                            {"if": {"row_index": "odd"}, "backgroundColor": "#f8f9fa"},
                            {"if": {"state": "selected"}, "backgroundColor": "transparent", "border": "none"},
                            {"if": {"state": "active"}, "backgroundColor": "transparent", "border": "none"},
                        ],
                        css=[
                            {"selector": ".dash-cell.focused", "rule": "outline: none !important; box-shadow: none !important; background-color: transparent !important;"},
                            {"selector": ".dash-cell.selected", "rule": "background-color: transparent !important;"},
                            {"selector": "td.dash-cell:focus", "rule": "outline: none !important; box-shadow: none !important;"},
                            {"selector": "td.dash-cell.focused", "rule": "background-color: transparent !important;"},
                        ],
                    ),
                ], className="p-3")
            ], className="shadow-sm h-100")
        ], lg=6, md=12, className="mb-4"),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🏃 Analyse des Athlètes", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Filtrez par sport pour explorer la distribution.", className="text-muted small mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Sport", className="fw-bold small"),
                            dcc.Dropdown(
                                id="sport-dropdown",
                                options=[{"label": "Tous les sports", "value": "ALL"}] + [{"label": s, "value": s} for s in sports],
                                value="ALL", clearable=False,
                            ),
                        ], md=6, className="mb-2"),
                        dbc.Col([
                            dbc.Label("Cap médailles", className="fw-bold small"),
                            html.P("Répartition du nombre de médailles par athlète selon le sport.", className="text-muted small mb-3"),
                            dcc.Slider(id="max-medals-slider", min=3, max=30, step=1, value=10, marks={i: str(i) for i in [3, 10, 20, 30]}),
                        ], md=6, className="mb-2"),
                    ]),
                    dcc.Graph(id="athlete-hist", style={"height": "280px"}, config={"displayModeBar": False}),
                ], className="p-3")
            ], className="shadow-sm h-100")
        ], lg=6, md=12, className="mb-4"),
    ], className="g-4"),

], style={"maxWidth": "1200px", "margin": "0 auto", "padding": "0 20px"}, className="bg-light")