import dash_bootstrap_components as dbc

NAVY_BLUE = "#2c3e50"


def create_navbar():
    """Barre de navigation."""
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("🏠 Accueil", href="/")),
            dbc.NavItem(dbc.NavLink("ℹ️ À Propos", href="/about")),
        ],
        brand="🏅 Dashboard Olympique",
        brand_href="/",
        color=NAVY_BLUE,
        dark=True,
        sticky="top",
        className="mb-4 shadow-sm"
    )