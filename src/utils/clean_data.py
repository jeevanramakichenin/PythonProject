import os
import pandas as pd

def clean_data():
    """
    Nettoie les données brutes de Spotify.
    - Supprime les lignes sans pays.
    - Convertit les dates au format datetime.
    - Sauvegarde le résultat dans data/cleaned/cleaned_data.csv.
    """
    # Définition des chemins
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_path = os.path.join(root_dir, 'data', 'raw', 'universal_top_spotify_songs.csv')
    cleaned_path = os.path.join(root_dir, 'data', 'cleaned', 'cleaned_data.csv')

    # Vérification que le fichier brut existe
    if not os.path.exists(raw_path):
        print(f"Erreur : Le fichier brut est introuvable : {raw_path}")
        return

    print("Début du nettoyage des données...")
    
    try:
        # Chargement des données
        df = pd.read_csv(raw_path)
        print(f"Taille initiale : {df.shape[0]} lignes")

        # Nettoyage
        
        # On supprime les lignes où la colonne 'country' est vide
        df = df.dropna(subset=['country'])
        
        # On transforme le texte "2023-10-25" en objet Date compréhensible par Python
        df['snapshot_date'] = pd.to_datetime(df['snapshot_date'])
        
        # Conversion de la durée (millisecondes à minutes)
        df['duration_min'] = df['duration_ms'] / 60000
        df = df.round({'duration_min': 2}) # On arrondit à 2 chiffres après la virgule

        print(f"Taille après nettoyage : {df.shape[0]} lignes")

        # On sauvegarde le fichier propre sans l'index
        df.to_csv(cleaned_path, index=False)
        print(f"Succès ! Données nettoyées sauvegardées ici : {cleaned_path}")

    except Exception as e:
        print(f"Une erreur est survenue pendant le nettoyage : {e}")

if __name__ == "__main__":
    clean_data()