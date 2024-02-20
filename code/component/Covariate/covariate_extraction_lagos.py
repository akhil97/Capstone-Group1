import os
# os.system("sudo pip install geopandas")
# os.system("sudo pip install rasterio")
#import geopandas as gpd
import rasterio
import numpy as np
import pandas as pd
from rasterio.plot import show, show_hist

############################################# COVARIATE DATA EXTRACTION ##############################################

LABEL_PATH = r'lag_covariate_compilation_53bands_clip.tif'

# Basic exploration and meta data
map_data = rasterio.open(LABEL_PATH)

# Read data from training tif and extract log, lat and label
for i in range(1, 54):
    band_data = map_data.read(i)
    no_data = map_data.nodata

    # Calculate the coordinates for the entire array once
    rows, cols = band_data.shape
    x_coords, y_coords = map_data.transform * np.meshgrid(np.arange(cols), np.arange(rows), indexing='xy')

    # Extracting data
    data = [{'long': x_coords[x, y], 'lat': y_coords[x, y], 'Band_{}'.format(i): band_data[x, y]}
            for x, y in np.ndindex(band_data.shape)
            if band_data[x, y] != no_data]

    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    print(len(df))
    df.to_csv('covariate_band_{}.csv'.format(i), index=False)

# Merge data from all bands into a single DataFrame
merged_df = None
for i in range(1, 54):
    band_df = pd.read_csv(f'covariate_band_{i}.csv')

    if merged_df is None:
        merged_df = band_df
    else:
        merged_df = pd.merge(merged_df, band_df, on=['long', 'lat'])

# Save the merged DataFrame to a CSV file
merged_df.to_csv('covariate_feature.csv', index=False)
