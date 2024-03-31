import os
import geopandas as gpd
import geowombat as gw
import pandas as pd
import glob
from concurrent.futures import ProcessPoolExecutor


def process_tif(tif_file, lagos_poly, output_dir):
    """
    Processes a given TIFF file by extracting information based on a provided geospatial polygon,
    and saves the extracted information to a CSV file.

    Args:
    tif_file (str): The path to the TIFF file to be processed.
    lagos_poly (GeoDataFrame): A GeoDataFrame containing the polygons to extract data within.
                                The geometry column should contain the polygons' centroids.
    output_dir (str): The directory path where the output CSV files will be saved.

    Returns:
    DataFrame: A pandas DataFrame containing the extracted information.
    """

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Open the TIFF file for reading
    with gw.open(tif_file) as src:

        # Extract data for the resampled contextual TIFF file within the provided polygon, handling nodata values
        df = gw.extract(src,
                        lagos_poly,
                        nodata=-9999)

        # Extract the feature name
        feature_name = os.path.splitext(os.path.basename(tif_file))[0]

        # Construct the output CSV file path
        output_csv_path = os.path.join(output_dir, f"{feature_name}_centroid.csv")

        # Save the extracted data to the CSV file
        df.to_csv(output_csv_path, index=False)

    return df


if __name__ == "__main__":
    gpkg_path = '/home/ubuntu/Cap2024/CapstoneDataset2024/Capstone_2024/Reference/Deprived_Areas/100mGrid_Lagos.gpkg'
    # Read the geospatial plygons from the GeoPackage
    lagos_poly = gpd.read_file(gpkg_path)
    # Calculate the centroids of the polygons
    lagos_poly["geometry"] = lagos_poly.centroid

    # Directory containing the TIFF files to be processed
    tif_directory = '/home/ubuntu/Cap2024/context/resampled_data'
    # Retrieve all TIFF file paths in the specified directory
    tif_files = glob.glob(os.path.join(tif_directory, '*.tif'))

    # Define the output folder where the CSV files will be saved
    output_dir = '/home/ubuntu/Cap2024/context/contextual_features_extraction'

    # Process each TIFF file in parallel, extract information and save each CSV in the specified folder
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_tif, tif_file, lagos_poly, output_dir) for tif_file in tif_files]

        for future in futures:
            future.result()
