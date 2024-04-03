import os
import glob
from concurrent.futures import ProcessPoolExecutor
import geopandas as gpd
import geowombat as gw


class TIFFProcessor:
    def __init__(self, gpkg_path, tif_directory, output_dir):
        self.gpkg_path = gpkg_path
        self.tif_directory = tif_directory
        self.output_dir = output_dir

    def process_tif(self, tif_file):
        """
        Processes a given TIFF file by extracting information based on a provided geospatial polygon,
        and saves the extracted information to a CSV file.

        Args:
        tif_file (str): The path to the TIFF file to be processed.

        Returns:
        DataFrame: A pandas DataFrame containing the extracted information.
        """

        # Read the geospatial polygons from the GeoPackage
        lagos_poly = gpd.read_file(self.gpkg_path)

        # Calculate the centroids of the polygons
        lagos_poly["geometry"] = lagos_poly.centroid

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Open the TIFF file for reading
        with gw.open(tif_file) as src:
            # Extract data for the resampled contextual TIFF file within the provided polygon, handling nodata values
            df = gw.extract(src,
                            lagos_poly,
                            nodata=-9999)

            # Extract the feature name
            feature_name = os.path.splitext(os.path.basename(tif_file))[0]

            # Construct the output CSV file path
            output_csv_path = os.path.join(self.output_dir, f"{feature_name}_centroid.csv")

            # Save the extracted data to the CSV file
            df.to_csv(output_csv_path, index=False)

        return df

    def process_all_tifs(self):
        # Retrieve all TIFF file paths in the specified directory
        tif_files = glob.glob(os.path.join(self.tif_directory, '*.tif'))

        # Process each TIFF file in parallel, extract information and save each CSV in the specified folder
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.process_tif, tif_file) for tif_file in tif_files]

            for future in futures:
                future.result()