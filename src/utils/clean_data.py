import os
import pandas as pd


def clean_data():
    """Nettoie les données des Jeux Olympiques."""
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_path = os.path.join(root_dir, 'data', 'raw', 'summer.csv')
    cleaned_path = os.path.join(root_dir, 'data', 'cleaned', 'cleaned_data.csv')

    if not os.path.exists(raw_path):
        print(f"Erreur : Le fichier '{raw_path}' est introuvable.")
        return

    print("Nettoyage des données...")

    try:
        df = pd.read_csv(raw_path)
        print(f"Taille initiale : {df.shape[0]} médailles")

        df.columns = [c.lower() for c in df.columns]
        df = df.dropna(subset=['country'])

        medal_score = {'Gold': 3, 'Silver': 2, 'Bronze': 1}
        df['score'] = df['medal'].map(medal_score)

        df.to_csv(cleaned_path, index=False)
        print(f"Données sauvegardées : {cleaned_path}")
        print(f"Taille finale : {df.shape[0]} médailles")

    except Exception as e:
        print(f"Erreur pendant le nettoyage : {e}")


if __name__ == "__main__":
    clean_data()