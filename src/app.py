from dash import Dash

#On initialise l'application Dash ici
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server