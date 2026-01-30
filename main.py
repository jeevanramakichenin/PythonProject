import os
import sys
from dash import html, dcc, Input, Output

from src.app import app
from src.pages import home, about
from src.components.navbar import create_navbar
from src.components.header import create_header
from src.components.footer import create_footer
from src.utils.get_data import get_data
from src.utils.clean_data import clean_data
from src.callbacks import register_callbacks


def main():
    print("Démarrage de l'application...")

    root_dir = os.path.dirname(os.path.abspath(__file__))
    cleaned_file = os.path.join(root_dir, "data", "cleaned", "cleaned_data.csv")
    kaggle_key = os.path.join(root_dir, "kaggle.json")

    if not os.path.exists(cleaned_file):
        print("Données manquantes. Vérification des sources...")

        if not os.path.exists(kaggle_key) and not os.path.exists(os.path.join(root_dir, "data", "cleaned")):
            print("ERREUR : 'kaggle.json' introuvable et aucune donnée locale.")
            print("Veuillez placer le fichier kaggle.json à la racine OU ajouter cleaned_data.csv dans data/cleaned/.")
            sys.exit(1)

        if os.path.exists(kaggle_key):
            print("Téléchargement des données brutes...")
            get_data()
            print("Nettoyage et traitement des données...")
            clean_data()
    else:
        print("Données détectées.")

    register_callbacks()

    app.layout = html.Div([
        dcc.Location(id="url", refresh=False),
        create_navbar(),
        create_header(),
        html.Div(id="page-content"),
        create_footer(),
    ])

    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def display_page(pathname):
        if pathname == "/about":
            return about.layout
        elif pathname == "/" or pathname is None:
            return home.layout
        return "404 - Page introuvable"

    print("Serveur lancé !")
    app.run(host="127.0.0.1", port=8050, debug=True, use_reloader=False)


if __name__ == "__main__":
    main()
