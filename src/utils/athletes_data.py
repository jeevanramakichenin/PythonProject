import os
import pandas as pd


def _load_cleaned() -> pd.DataFrame:
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    cleaned_path = os.path.join(root_dir, "data", "cleaned", "cleaned_data.csv")
    df = pd.read_csv(cleaned_path)
    df = df.dropna(subset=["athlete", "medal", "sport"])
    return df


def get_sports_list():
    """Retourne la liste des sports disponibles."""
    df = _load_cleaned()
    return sorted(df["sport"].dropna().unique().tolist())


def get_years_list():
    """Retourne la liste des années olympiques."""
    df = _load_cleaned()
    return sorted(df["year"].dropna().unique().tolist())


def medals_per_athlete_by_sport(sport: str | None):
    """Compte les médailles par athlète, filtré par sport."""
    df = _load_cleaned()

    if sport and sport != "ALL":
        df = df[df["sport"] == sport]

    medals = (
        df.groupby("athlete")
          .size()
          .reset_index(name="medal_count")
          .sort_values("medal_count", ascending=False)
    )
    return medals
