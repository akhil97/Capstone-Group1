import os
import geopandas as gpd
import geowombat as gw
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Extractor:
    def __init__(self, poly_file, raster_file, output_file):
        """
        Initialize the Extractor object with file paths for the polygon, raster, and output files.
        Args:
        poly_file (str): Path to the GeoPackage file containing polygons.
        raster_file (str): Path to the raster file.
        output_file (str): Path to the output CSV file where extracted data will be saved.
        """
        self.poly_file = os.path.join(os.getcwd(), poly_file)
        self.raster_file = os.path.join(os.getcwd(), raster_file)
        self.output_file = os.path.join(os.getcwd(), output_file)

    def extract_data(self):
        """
        Extract data from a raster file using polygon centroids as the reference points.
        The function reads the polygon file, replaces polygons with their centroids,
        extracts the raster data at these centroid locations, and saves the data to a CSV file.
        """
        logging.info(f'Starting data extraction...')
        try:
            # Read a GeoPackage containing polygons and slum labels
            lagos_poly = gpd.read_file(self.poly_file)

            # Replace the geometry of each polygon with its centroid
            lagos_poly["geometry"] = lagos_poly.centroid

            # Open a raster file that contains covariate data for Lagos with 53 bands
            with gw.open(self.raster_file) as src:
                logging.info(f'Raster file {self.raster_file} opened successfully.')
                # Extract raster values using the centroids of the polygons defined in 'lagos_poly'
                df = gw.extract(
                    src,
                    lagos_poly,
                    nodata=-9999,
                )
                logging.info('Data extraction from raster file completed.')

                # Save the extracted data to a CSV file which has included slum labels
                df.to_csv(self.output_file, index=False)
                logging.info(f'Covariate CSV saved successfully to {self.output_file}')

        except Exception as e:
            logging.error(f'Error during extraction: {e}')
