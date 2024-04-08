import os
import glob
from concurrent.futures import ProcessPoolExecutor
import geopandas as gpd
import geowombat as gw
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TIFFProcessor:
    def __init__(self, gpkg_path, tif_directory, output_dir):
        self.gpkg_path = gpkg_path
        self.tif_directory = tif_directory
        self.output_dir = output_dir
        self.lagos_poly = self.read_and_extract_polygons()

    def read_and_extract_polygons(self):
        logging.info(f"Loading polygons from {self.gpkg_path}")

        # Read the geospatial polygons from the GeoPackage
        lagos_poly = gpd.read_file(self.gpkg_path)
        # Calculate the centroids of the polygons
        lagos_poly["geometry"] = lagos_poly.centroid
        return lagos_poly

    def get_tiff_files(self):
        """
        Get TIFF files from subdirectories.

        Returns:
            List of paths to TIFF files found within the specified directory and its subdirectories.
        """
        logging.info(f"Scanning for TIFF files in {self.tif_directory}")
        tiff_files = []
        for dirpath, _, filenames in os.walk(self.tif_directory):
            for filename in filenames:
                if filename.endswith('.tif'):
                    tiff_files.append(os.path.join(dirpath, filename))
        logging.info(f"Found {len(tiff_files)} TIFF files")
        return tiff_files

    def process_tif(self, tif_file):
        """
        Processes a given TIFF file by extracting information based on the previously loaded geospatial polygon,
        and saves the extracted information to a CSV file.

        Args:
        tif_file (str): The path to the TIFF file to be processed.
        """
        logging.info(f"Processing TIFF file: {tif_file}")
        try:
            # Ensure the output directory exists
            os.makedirs(self.output_dir, exist_ok=True)

            # Open the TIFF file for reading
            with gw.open(tif_file) as src:
                df = gw.extract(src,
                                self.lagos_poly,
                                nodata=-9999)

                # Extract the feature name
                feature_name = os.path.splitext(os.path.basename(tif_file))[0]

                # Construct the output CSV file path
                output_csv_path = os.path.join(self.output_dir, f"{feature_name}_centroid.csv")

                # Save the extracted data to the CSV file
                df.to_csv(output_csv_path, index=False)

            logging.info(f"Successfully processed and saved data from {tif_file}")
        except Exception as e:
            logging.error(f"Error processing file {tif_file}: {e}")

        return df

    def process_all_tifs(self):
        logging.info("Starting the TIFF processing workflow.")

        # Retrieve all TIFF file paths in the specified directory
        tif_files = self.get_tiff_files()

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.process_tif, tif_file) for tif_file in tif_files]
            for future in futures:
                future.result()
        logging.info("Completed all TIFF processing.")
