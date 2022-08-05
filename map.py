import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])


map = folium.Map(location=[39.58, -99.09], zoom_start=6, tiles="Stamen Terrain")

fg_US_Volcanoes = folium.FeatureGroup(name="US Volcanoes")

for lt, ln, el in zip(lat, lon, elev):
    fg_US_Volcanoes.add_child(
        folium.CircleMarker(
            location=[lt, ln],
            radius=6,
            popup=str(el) + "m",
            fill_color="green"
            if el < 1000
            else "orange"
            if 1000 < el < 3000
            else "red",
            color="black",
            fill_opacity=0.7,
        )
    )

fg_Population = folium.FeatureGroup(name="Country Population")
fg_Population.add_child(
    folium.GeoJson(
        data=open("world.json", "r", encoding="utf-8-sig").read(),
        style_function=lambda x: {
            "fillColor": "green"
            if x["properties"]["POP2005"] < 10000000
            else "orange"
            if 10000000 < x["properties"]["POP2005"] < 20000000
            else "red"
        },
    )
)

map.add_child(fg_US_Volcanoes)
map.add_child(fg_Population)

map.add_child(folium.LayerControl())

map.save("index.html")
