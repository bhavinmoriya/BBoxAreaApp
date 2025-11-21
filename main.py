from pyproj import Transformer
boundingbox = ['48.6858724', '48.6859994', '9.3646052', '9.3647929']
# [min_lat, max_lat, min_lon, max_lon]
min_lat, max_lat = map(float, boundingbox[:2])
min_lon, max_lon = map(float, boundingbox[2:])

# Define a transformer to project lat/lon to UTM (meters)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32632", always_xy=True)  # UTM zone for Esslingen, Germany

# Convert all four corners
min_x, min_y = transformer.transform(min_lon, min_lat)
max_x, max_y = transformer.transform(max_lon, max_lat)

# Calculate width and height in meters
width = max_x - min_x
height = max_y - min_y

# Area in square meters
area_sq_m = width * height
print(f"Area: {area_sq_m:.2f} sq m")
