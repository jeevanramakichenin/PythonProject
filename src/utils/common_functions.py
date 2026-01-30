import os
import pandas as pd


def load_data():
    """Charge les données nettoyées."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(current_dir))
    file_path = os.path.join(root_dir, 'data', 'cleaned', 'cleaned_data.csv')

    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()