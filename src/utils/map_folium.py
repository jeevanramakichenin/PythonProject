import os
import json
import pandas as pd
import folium as fl


def _detect_key_on(geojson_path: str) -> str:
    """
    Détecte automatiquement la bonne clé key_on pour Folium Choropleth.
    Priorité: feature.id, puis plusieurs noms courants dans properties.
    """
    with open(geojson_path, "r", encoding="utf-8") as f:
        gj = json.load(f)

    feat = gj["features"][0]

    if "id" in feat:
        return "feature.id"

    props = feat.get("properties", {}) or {}

    candidates = ["iso_a3", "ISO_A3", "ADM0_A3", "adm0_a3", "id", "ISO3", "iso3"]
    for c in candidates:
        if c in props:
            return f"feature.properties.{c}"

    if "name" in props:
        return "feature.properties.name"

    raise ValueError("Impossible de détecter la clé ISO dans le GeoJSON.")


def build_medals_map_html() -> str:
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    cleaned_path = os.path.join(root_dir, "data", "cleaned", "cleaned_data.csv")
    geojson_path = os.path.join(root_dir, "data", "geo", "world-countries.json")

    df = pd.read_csv(cleaned_path)
    df = df.dropna(subset=["country", "medal"])

    country_medals = (
        df.groupby(["country", "medal"])
        .size()
        .unstack(fill_value=0)
    )

    for col in ["Gold", "Silver", "Bronze"]:
        if col not in country_medals.columns:
            country_medals[col] = 0

    country_medals["Total"] = country_medals[["Gold", "Silver", "Bronze"]].sum(axis=1)
    country_medals = country_medals[country_medals["Total"] > 0]

    for medal in ["Gold", "Silver", "Bronze"]:
        country_medals[f"{medal}_pct"] = country_medals[medal] / country_medals["Total"] * 100

    country_medals = country_medals.reset_index()
    data = country_medals[["country", "Gold_pct", "Silver_pct", "Bronze_pct"]]

    m = fl.Map(location=[20, 0], zoom_start=2, tiles="cartodbpositron")

    key_on = _detect_key_on(geojson_path)
    print(f"[folium] key_on détecté: {key_on}")

    fl.Choropleth(
        geo_data=geojson_path,
        name="Or",
        data=data,
        columns=["country", "Gold_pct"],
        key_on=key_on,
        fill_color="YlOrRd",
        fill_opacity=0.85,
        line_opacity=0.3,
        nan_fill_color="white",
        nan_fill_opacity=1,
        legend_name="% de médailles d'or",
    ).add_to(m)

    fl.Choropleth(
        geo_data=geojson_path,
        name="Argent",
        data=data,
        columns=["country", "Silver_pct"],
        key_on=key_on,
        fill_color="Greys",
        fill_opacity=0.85,
        line_opacity=0.3,
        nan_fill_color="white",
        nan_fill_opacity=1,
        legend_name="% de médailles d'argent",
    ).add_to(m)

    fl.Choropleth(
        geo_data=geojson_path,
        name="Bronze",
        data=data,
        columns=["country", "Bronze_pct"],
        key_on=key_on,
        fill_color="Oranges",
        fill_opacity=0.85,
        line_opacity=0.3,
        nan_fill_color="white",
        nan_fill_opacity=1,
        legend_name="% de médailles de bronze",
    ).add_to(m)

    fl.LayerControl().add_to(m)
    return m.get_root().render()

