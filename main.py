import os
import sys
from dash import html, dcc, Input, Output

# Imports du projet
from src.app import app
from src.pages import home, about
from src.components.navbar import create_navbar
from src.utils.get_data import get_data
from src.utils.clean_data import clean_data
from src.callbacks import register_callbacks


def main():
    print("Démarrage de l'application...")

    # --- VÉRIFICATION DES DONNÉES ---
    root_dir = os.path.dirname(os.path.abspath(__file__))
    cleaned_file = os.path.join(root_dir, "data", "cleaned", "cleaned_data.csv")
    kaggle_key = os.path.join(root_dir, "kaggle.json")

    if not os.path.exists(cleaned_file):
        print("Données manquantes. Vérification des sources...")

        # Si pas de données locales et pas de clé Kaggle, on stop
        if not os.path.exists(kaggle_key) and not os.path.exists(os.path.join(root_dir, "data", "cleaned")):
            print("ERREUR : 'kaggle.json' introuvable et aucune donnée locale.")
            print("Veuillez placer le fichier kaggle.json à la racine OU ajouter cleaned_data.csv dans data/cleaned/.")
            sys.exit(1)

        # Si la clé Kaggle est présente, on télécharge puis on nettoie
        if os.path.exists(kaggle_key):
            print("Téléchargement des données brutes...")
            get_data()

            print("Nettoyage et traitement des données...")
            clean_data()
    else:
        print("Données détectées.")

    # --- ENREGISTREMENT DES CALLBACKS (IMPORTANT) ---
    register_callbacks()

    # --- CONFIGURATION DE LA NAVIGATION ---
    app.layout = html.Div([
        dcc.Location(id="url", refresh=False),
        create_navbar(),
        html.Div(id="page-content"),
    ])

    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def display_page(pathname):
        if pathname == "/about":
            return about.layout
        elif pathname == "/" or pathname is None:
            return home.layout
        return "404 - Page introuvable"

    # --- LANCEMENT ---
    # Codespaces -> host=0.0.0.0 pour que le port soit accessible
    print("Serveur lancé !")
    app.run(host="0.0.0.0", port=8050, debug=True)


if __name__ == "__main__":
    main()
