import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
from pathlib import Path

# Load your data
merged_contextual_features_df = pd.read_csv('merged_contextual_features.csv')

file_path = Path('/home/ubuntu/Cap2024/reference/coordinates.csv')
coordinates_df = pd.read_csv(file_path)
# print(coordinates_df.columns)


# Convert the DataFrame to a GeoDataFrame
gdf_merged_contextual_features = gpd.GeoDataFrame(
    merged_contextual_features_df,
    geometry=[Point(xy) for xy in zip(merged_contextual_features_df.longitude, merged_contextual_features_df.latitude)]
)

gdf_coordinates = gpd.GeoDataFrame(
    coordinates_df,
    geometry=[Point(xy) for xy in zip(coordinates_df['new_long'], coordinates_df['new_lat'])]
)


# Set a coordinate reference system (CRS)
# It's essential to make sure both GeoDataFrames use the same CRS
# EPSG:4326 is a common geographic coordinate system (latitude, longitude)
gdf_merged_contextual_features.crs = "EPSG:4326"
gdf_coordinates.crs = "EPSG:4326"

# Perform the spatial join
# This example assumes you want to find points from gdf_coordinates that fall within the locations in gdf_merged_contextual_features
# Adjust 'op' as needed for your specific spatial relationship ('intersects', 'contains', 'within', etc.)
joined_gdf = gpd.sjoin(gdf_coordinates, gdf_merged_contextual_features, how="inner", op="intersects")

# Save the result to a new CSV
joined_gdf.to_csv('joined_data.csv', index=False)
