import os
import pandas as pd

def clean_data():
    """
    Nettoie les données des Jeux Olympiques (summer.csv).
    """
    #Chemins
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_path = os.path.join(root_dir, 'data', 'raw', 'summer.csv')
    cleaned_path = os.path.join(root_dir, 'data', 'cleaned', 'cleaned_data.csv')

    #Vérification
    if not os.path.exists(raw_path):
        print(f"Erreur : Le fichier '{raw_path}' est introuvable.")
        return

    print("Nettoyage des données Olympiques (Summer)...")

    try:
        #Chargement
        df = pd.read_csv(raw_path)
        print(f"Taille initiale : {df.shape[0]} médailles")

        #Renommage des colonnes (tout en minuscules pour coder plus vite)
        df.columns = [c.lower() for c in df.columns]

        #Nettoyage spécifique
        # On vérifie qu'il n'y a pas de pays manquant pour la carte
        df = df.dropna(subset=['country'])

        #Ajout d'une colonne "Valeur" pour convertir les medailles en scores
        medal_score = {'Gold': 3, 'Silver': 2, 'Bronze': 1}
        df['score'] = df['medal'].map(medal_score)

        #Sauvegarde
        df.to_csv(cleaned_path, index=False)
        print(f"Données propres sauvegardées dans : {cleaned_path}")
        print(f"Colonnes disponibles : {list(df.columns)}")
        print(f"Taille finale : {df.shape[0]} médailles")

    except Exception as e:
        print(f"Erreur pendant le nettoyage : {e}")


if __name__ == "__main__":
    clean_data()