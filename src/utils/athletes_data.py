import os
import pandas as pd


def _load_cleaned() -> pd.DataFrame:
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    cleaned_path = os.path.join(root_dir, "data", "cleaned", "cleaned_data.csv")
    df = pd.read_csv(cleaned_path)
    df = df.dropna(subset=["athlete", "medal", "sport"])
    return df


def get_sports_list():
    df = _load_cleaned()
    sports = sorted(df["sport"].dropna().unique().tolist())
    return sports


def medals_per_athlete_by_sport(sport: str | None):
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
