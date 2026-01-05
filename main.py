import os
import sys
from dash import html, dcc, Input, Output

#Imports du projet
from src.app import app
from src.pages import home, about
from src.components.navbar import create_navbar
from src.utils.get_data import get_data
from src.utils.clean_data import clean_data


def main():
    print("Démarrage de l'application...")

    #---VÉRIFICATION DES DONNÉES---
    root_dir = os.path.dirname(os.path.abspath(__file__))
    cleaned_file = os.path.join(root_dir, 'data', 'cleaned', 'cleaned_data.csv')
    kaggle_key = os.path.join(root_dir, 'kaggle.json')

    if not os.path.exists(cleaned_file):
        print("Données manquantes...")
        if not os.path.exists(kaggle_key) and not os.path.exists(os.path.join(root_dir, 'data', 'cleaned')):
            print("ERREUR : Pas de clé kaggle et pas de données.")
            sys.exit(1)
        if os.path.exists(kaggle_key):
            get_data()
            clean_data()
    else:
        print("Données détectées.")


    #---CONFIGURATION DE LA NAVIGATION---

    #On définit la structure globale du site
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False), #surveille l'URL
        create_navbar(),

        #Le conteneur qui change selon la page
        html.Div(id='page-content')
    ])

    # --- 3. LE CERVEAU (CALLBACK) ---

    #Cette fonction est appelée chaque fois que l'URL change
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/about':
            return about.layout
        elif pathname == '/':
            return home.layout
        else:
            return "404 - Page introuvable"

    #---LANCEMENT---
    print("Serveur lancé ! Clique ici : http://127.0.0.1:8050/")
    app.run(debug=True)


if __name__ == "__main__":
    main()