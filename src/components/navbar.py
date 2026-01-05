from dash import html, dcc


def create_navbar():

    layout = html.Div([
        #Lien vers l'accueil
        dcc.Link('🏠 Accueil', href='/', style={
            'marginRight': '20px',
            'textDecoration': 'none',
            'fontSize': '18px',
            'color': 'black'
        }),

        # Lien vers le A Propos
        dcc.Link('ℹ️ À Propos', href='/about', style={
            'textDecoration': 'none',
            'fontSize': '18px',
            'color': 'black'
        })
    ], style={
        'padding': '15px 30px',
        'backgroundColor': '#f0f0f0',
        'borderBottom': '1px solid #ccc',
        'marginBottom': '20px'
    })

    return layout