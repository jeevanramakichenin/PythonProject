import pandas as pd
import os

def load_data():
    #Fonction pour charger les données nettoyées.

    #On récupère le chemin absolu du fichier actuel
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(current_dir))
    file_path = os.path.join(root_dir, 'data', 'cleaned', 'cleaned_data.csv')

    #sécurité pour si le fichier n'est pas encore là
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()