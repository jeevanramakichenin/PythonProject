import os
import json
import pandas as pd
import folium as fl
from branca.element import MacroElement, Template

NAVY_BLUE = "#2c3e50"
GOLD = "#d4af37"


def _detect_key_on(geojson_path: str) -> str:
    """Détecte la bonne clé pour Folium Choropleth."""
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

    df = pd.read_csv(cleaned_path).dropna(subset=["country", "medal"])

    country_medals = df.groupby(["country", "medal"]).size().unstack(fill_value=0)
    for col in ["Gold", "Silver", "Bronze"]:
        if col not in country_medals.columns:
            country_medals[col] = 0

    country_medals["Total"] = country_medals[["Gold", "Silver", "Bronze"]].sum(axis=1)
    country_medals = country_medals[country_medals["Total"] > 0]

    for medal in ["Gold", "Silver", "Bronze"]:
        country_medals[f"{medal}_pct"] = country_medals[medal] / country_medals["Total"] * 100

    country_medals = country_medals.reset_index()
    data = country_medals[["country", "Gold_pct", "Silver_pct", "Bronze_pct"]]

    m = fl.Map(location=[20, 0], zoom_start=2, tiles=None)

    attr = "© OpenStreetMap contributors © CARTO"
    fl.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png",
        attr=attr,
        control=False,
        show=True,
    ).add_to(m)

    class _LabelsPane(MacroElement):
        def __init__(self):
            super().__init__()
            self._name = "LabelsPane"
            self._template = Template("""
            {% macro script(this, kwargs) %}
            var map = {{ this._parent.get_name() }};
            map.createPane('labels');
            map.getPane('labels').style.zIndex = 650;
            map.getPane('labels').style.pointerEvents = 'none';
            {% endmacro %}
            """)

    m.add_child(_LabelsPane())

    fl.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}{r}.png",
        attr=attr,
        overlay=True,
        control=False,
        show=True,
        pane="labels",
    ).add_to(m)

    key_on = _detect_key_on(geojson_path)

    LEG_GOLD = "% de médailles d'or"
    LEG_SILVER = "% de médailles d'argent"
    LEG_BRONZE = "% de médailles de bronze"

    gold_layer = fl.Choropleth(
        geo_data=geojson_path,
        name="🥇 Or",
        data=data,
        columns=["country", "Gold_pct"],
        key_on=key_on,
        fill_color="YlOrBr",
        fill_opacity=0.8,
        line_opacity=0.6,
        line_color=NAVY_BLUE,
        nan_fill_color="#f8f9fa",
        legend_name=LEG_GOLD,
        show=False,
        overlay=True,
        control=True,
    ).add_to(m)

    silver_layer = fl.Choropleth(
        geo_data=geojson_path,
        name="🥈 Argent",
        data=data,
        columns=["country", "Silver_pct"],
        key_on=key_on,
        fill_color="Blues",
        fill_opacity=0.8,
        line_opacity=0.6,
        line_color=NAVY_BLUE,
        nan_fill_color="#f8f9fa",
        legend_name=LEG_SILVER,
        show=False,
        overlay=True,
        control=True,
    ).add_to(m)

    bronze_layer = fl.Choropleth(
        geo_data=geojson_path,
        name="🥉 Bronze",
        data=data,
        columns=["country", "Bronze_pct"],
        key_on=key_on,
        fill_color="Oranges",
        fill_opacity=0.8,
        line_opacity=0.6,
        line_color=NAVY_BLUE,
        nan_fill_color="#f8f9fa",
        legend_name=LEG_BRONZE,
        show=True,
        overlay=True,
        control=True,
    ).add_to(m)

    fl.LayerControl(collapsed=False).add_to(m)

    class LegendAndRadioToggle(MacroElement):
        def __init__(self, gold, silver, bronze, leg_gold, leg_silver, leg_bronze):
            super().__init__()
            self._name = "LegendAndRadioToggle"
            self.gold = gold.get_name()
            self.silver = silver.get_name()
            self.bronze = bronze.get_name()
            self.leg_gold = json.dumps(leg_gold)
            self.leg_silver = json.dumps(leg_silver)
            self.leg_bronze = json.dumps(leg_bronze)

            self._template = Template("""
            {% macro script(this, kwargs) %}
            var map = {{ this._parent.get_name() }};
            var GOLD = {{ this.gold }};
            var SILVER = {{ this.silver }};
            var BRONZE = {{ this.bronze }};

            var LEG_GOLD = {{ this.leg_gold }};
            var LEG_SILVER = {{ this.leg_silver }};
            var LEG_BRONZE = {{ this.leg_bronze }};

            function getLegendSvgs() {
              return document.querySelectorAll('.legend.leaflet-control svg') || [];
            }

            function setLegend(caption) {
              var svgs = getLegendSvgs();
              svgs.forEach(function(svg){
                var cap = svg.querySelector('text.caption');
                var txt = cap ? (cap.textContent || '').trim() : '';
                svg.style.display = (txt === caption) ? 'block' : 'none';
              });
            }

            function enforceExclusive(activeLayer) {
              if (activeLayer === GOLD) { map.removeLayer(SILVER); map.removeLayer(BRONZE); setLegend(LEG_GOLD); }
              if (activeLayer === SILVER) { map.removeLayer(GOLD); map.removeLayer(BRONZE); setLegend(LEG_SILVER); }
              if (activeLayer === BRONZE) { map.removeLayer(GOLD); map.removeLayer(SILVER); setLegend(LEG_BRONZE); }
            }

            function convertOverlayCheckboxesToRadios() {
              var box = document.querySelector('.leaflet-control-layers-overlays');
              if (!box) return;
              var inputs = box.querySelectorAll('input[type="checkbox"]');
              inputs.forEach(function(inp){
                inp.type = 'radio';
                inp.name = 'medal_choice';
              });
            }

            setTimeout(function() {
              convertOverlayCheckboxesToRadios();
              setLegend(LEG_BRONZE);
            }, 250);

            map.on('overlayadd', function(e) {
              enforceExclusive(e.layer);
              setTimeout(convertOverlayCheckboxesToRadios, 0);
            });

            {% endmacro %}
            """)

    m.add_child(LegendAndRadioToggle(
        gold_layer, silver_layer, bronze_layer,
        LEG_GOLD, LEG_SILVER, LEG_BRONZE
    ))

    return m.get_root().render()