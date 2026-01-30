from dash import html
import dash_bootstrap_components as dbc


def create_footer():
    """Pied de page commun à toutes les pages."""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Hr(className="mt-4"),
                html.P("© 2026 Jeevan RAMAKICHENIN & Ilo RABIARIVELO — Projet ESIEE Paris", className="text-center text-muted small mb-3")
            ], width=12)
        ]),
    ], fluid=True)
