import os
import sys

# On importe tes fonctions qu'on a créées plus tôt
from src.utils.get_data import get_data
from src.utils.clean_data import clean_data

def main():
    print("Démarrage de l'application Data Project...")

    # Définition des chemins
    root_dir = os.path.dirname(os.path.abspath(__file__))
    cleaned_file = os.path.join(root_dir, 'data', 'cleaned', 'cleaned_data.csv')
    kaggle_key = os.path.join(root_dir, 'kaggle.json')

    # Vérification du fichier cleaned file
    if not os.path.exists(cleaned_file):
        print("⚠️  Données manquantes. Lancement de la récupération automatique...")
        
        # On Vérifie si on a la clé pour télécharger
        if not os.path.exists(kaggle_key):
            print("ERREUR CRITIQUE : Fichier 'kaggle.json' manquant.")
            print("   Impossible de télécharger les données sans la clé.")
            print("   Veuillez placer 'kaggle.json' à la racine du projet.")
            sys.exit(1)
        
        # Si on a la clé, on lance les scripts l'un après l'autre
        print("Téléchargement des données brutes...")
        get_data()
        
        print("Nettoyage des données...")
        clean_data()
    else:
        print("Données détectées. Pas besoin de retélécharger.")
    
    print("Bravo, tout est carré !")

if __name__ == "__main__":
    main()