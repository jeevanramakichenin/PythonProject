import os
import sys

# Imports des modules du projet
from src.app import app
from src.pages import home
from src.utils.get_data import get_data
from src.utils.clean_data import clean_data
from src.utils.map_folium import build_medals_map_html
from src.callbacks import register_callbacks



def main():
    print("Demarrage de l'application...")

    # Definition des chemins absolus
    root_dir = os.path.dirname(os.path.abspath(__file__))
    cleaned_file = os.path.join(root_dir, 'data', 'cleaned', 'cleaned_data.csv')
    kaggle_key = os.path.join(root_dir, 'kaggle.json')

    # Verification de la presence des donnees
    if not os.path.exists(cleaned_file):
        print("Donnees manquantes. Verification des sources...")

        # Arret si ni les donnees ni la cle ne sont presentes
        if not os.path.exists(kaggle_key) and not os.path.exists(os.path.join(root_dir, 'data', 'cleaned')):
            print("Erreur : 'kaggle.json' introuvable et aucune donnee locale.")
            print("Veuillez placer le fichier kaggle.json a la racine.")
            sys.exit(1)

        # Execution de la pipeline de donnees si la cle est presente
        if os.path.exists(kaggle_key):
            print("Telechargement des donnees brutes...")
            get_data()

            print("Nettoyage et traitement des donnees...")
            clean_data()
    else:
        print("Donnees detectees.")

    # Appel des callback
    register_callbacks()

    # Configuration et lancement du serveur Dash
    # On charge le layout de la page d'accueil

    app.layout = home.layout
    app.run(debug=True)


if __name__ == "__main__":
    main()