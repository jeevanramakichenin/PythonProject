import os


def get_data():
    """Télécharge le dataset Jeux Olympiques depuis Kaggle."""
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_data_path = os.path.join(root_dir, 'data', 'raw')
    kaggle_config_path = os.path.join(root_dir, 'kaggle.json')

    if not os.path.exists(kaggle_config_path):
        print(f"Erreur : kaggle.json introuvable ici : {kaggle_config_path}")
        return

    os.environ['KAGGLE_CONFIG_DIR'] = root_dir
    from kaggle.api.kaggle_api_extended import KaggleApi

    dataset_name = "the-guardian/olympic-games"
    print(f"Téléchargement de : {dataset_name}...")

    try:
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files(dataset_name, path=raw_data_path, unzip=True)
        print(f"Fichiers téléchargés dans : {raw_data_path}")
    except Exception as e:
        print(f"Erreur : {e}")