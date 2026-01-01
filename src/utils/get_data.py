import os

def get_data():
    """
    Télécharge le dataset Spotify depuis Kaggle via l'API.
    Les données sont stockées dans data/raw/.
    """
    # Configuration des chemins
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_data_path = os.path.join(root_dir, 'data', 'raw')
    kaggle_config_path = os.path.join(root_dir, 'kaggle.json')

    # Vérification de sécurité
    if not os.path.exists(kaggle_config_path):
        print(f"Erreur : kaggle.json introuvable ici : {kaggle_config_path}")
        return

    # Configuration de l'environnement
    os.environ['KAGGLE_CONFIG_DIR'] = root_dir

    # On fait l'impoirt maintenant comme ça le chemin sera bien celui qu'on à définit au dessus
    from kaggle.api.kaggle_api_extended import KaggleApi

    # Authentification et Téléchargement
    dataset_name = "the-guardian/olympic-games"
    print(f"🔄 Connexion à Kaggle et téléchargement de : {dataset_name}...")
    
    try:
        api = KaggleApi()
        api.authenticate()
        
        # Téléchargement
        api.dataset_download_files(dataset_name, path=raw_data_path, unzip=True)
        
        print(f"Succès ! Les fichiers sont dans : {raw_data_path}")
        print("Liste des fichiers :", os.listdir(raw_data_path))
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    get_data()