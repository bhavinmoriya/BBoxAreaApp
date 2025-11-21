import streamlit as st
import folium
from folium import plugins
from pyproj import Transformer
from streamlit_folium import st_folium

# Title
st.title("Bounding Box Area Calculator")

# Input: Bounding Box
st.sidebar.header("Input Bounding Box")
boundingbox_input = st.sidebar.text_input(
    "Enter bounding box as `min_lat, max_lat, min_lon, max_lon` (comma-separated):",
    value="48.6858724, 48.6859994, 9.3646052, 9.3647929"
)

# Parse input
try:
    min_lat, max_lat, min_lon, max_lon = map(float, boundingbox_input.split(","))
    boundingbox = [min_lat, max_lat, min_lon, max_lon]
except ValueError:
    st.error("Invalid input. Please enter 4 comma-separated numbers.")
    st.stop()

# Calculate area
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32632", always_xy=True)
min_x, min_y = transformer.transform(min_lon, min_lat)
max_x, max_y = transformer.transform(max_lon, max_lat)
width = max_x - min_x
height = max_y - min_y
area_sq_m = width * height

# Display results
st.subheader("Results")
st.write(f"**Bounding Box Coordinates:** {boundingbox}")
st.write(f"**Area:** {area_sq_m:.2f} Square meters.")

# Create Folium map
m = folium.Map(
    location=[(min_lat + max_lat) / 2, (min_lon + max_lon) / 2],
    zoom_start=18,
    tiles="OpenStreetMap"
)

# Add bounding box rectangle
folium.Rectangle(
    bounds=[[min_lat, min_lon], [max_lat, max_lon]],
    color="red",
    fill=True,
    fill_color="blue",
    fill_opacity=0.2,
).add_to(m)

# Add markers for corners
for lat, lon in [
    (min_lat, min_lon),
    (min_lat, max_lon),
    (max_lat, min_lon),
    (max_lat, max_lon),
]:
    folium.Marker([lat, lon]).add_to(m)

# Display map in Streamlit
st_folium(m, width=700, height=500)
