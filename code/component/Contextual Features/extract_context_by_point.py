import os
import geopandas as gpd
import geowombat as gw
import pandas as pd
import glob
from concurrent.futures import ProcessPoolExecutor


def process_tif(tif_file, lagos_poly, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    with gw.open(tif_file) as src:
        # Extract data for the resampled contextual TIFF file
        df = gw.extract(src,
                        lagos_poly,
                        nodata=-9999)

        # Extract the feature name
        feature_name = os.path.splitext(os.path.basename(tif_file))[0]

        # Construct the output CSV file path
        output_csv_path = os.path.join(output_dir, f"{feature_name}_centroid.csv")

        # Save the DataFrame to the CSV file in the specified folder
        df.to_csv(output_csv_path, index=False)

    return df


if __name__ == "__main__":
    gpkg_path = '/home/ubuntu/Cap2024/CapstoneDataset2024/Capstone_2024/Reference/Deprived_Areas/100mGrid_Lagos.gpkg'
    lagos_poly = gpd.read_file(gpkg_path)
    lagos_poly["geometry"] = lagos_poly.centroid

    tif_directory = '/home/ubuntu/Cap2024/context/resampled_data'
    tif_files = glob.glob(os.path.join(tif_directory, '*.tif'))

    # Define the output folder where the CSV files will be saved
    output_dir = '/home/ubuntu/Cap2024/context/contextual_features_extraction'

    # Process TIFF files in parallel and save CSVs in the specified folder
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_tif, tif_file, lagos_poly, output_dir) for tif_file in tif_files]

        for future in futures:
            future.result()
