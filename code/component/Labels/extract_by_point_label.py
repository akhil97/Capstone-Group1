import geopandas as gpd
import geowombat as gw
import pandas as pd
import os

# Path to the directory containing TIFF files
tif_dir = '/home/ubuntu/Cap2024/Nairobi/nairobi_mask_100m'
tif_files = [os.path.join(tif_dir, f) for f in os.listdir(tif_dir) if f.endswith('.tif')]

# Read a GeoPackage containing polygons for Nairobi
nairobi_poly = gpd.read_file("100mGrid_Nairobi.gpkg")
# Replace the geometry of each polygon with its centroid
nairobi_poly["geometry"] = nairobi_poly.centroid

# Initialize an empty DataFrame to collect data from all TIFF files
all_data = pd.DataFrame()

for tif_file in tif_files:
    with gw.open(tif_file) as src:
        # Extract raster values using the centroids of the polygons defined in 'nairobi_poly'
        df = gw.extract(
            src,
            nairobi_poly,
            nodata=-9999,
        )

        # Append the extracted data to the all_data DataFrame
        all_data = pd.concat([all_data, df], ignore_index=True)


# Rename column '1' to 'label'
all_data.rename(columns={1: 'label'}, inplace=True)

# Convert the "label" column to integers
all_data['label'] = all_data['label'].astype(int)

# Save the aggregated extracted data to a CSV file
all_data.to_csv("nairobi_centroid_label.csv", index=False)


