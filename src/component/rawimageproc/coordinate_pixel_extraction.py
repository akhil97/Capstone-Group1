import os
import geopandas as gpd
import geowombat as gw
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExtractRasterValues:
    def __init__(self, gpkg_file, tif_file, output_csv):
        """
        Initialize the ExtractRasterValues object with file paths for the GeoPackage, TIFF file,
        and the output CSV file.

        Args:
        gpkg_file (str): Path to the GeoPackage file containing polygons.
        tif_file (str): Path to the TIFF file containing raster data.
        output_csv (str): Path where the extracted values will be saved as CSV.
        """
        self.gpkg_file = os.path.join(os.getcwd(), gpkg_file)
        self.tif_file = os.path.join(os.getcwd(), tif_file)
        self.output_csv = os.path.join(os.getcwd(), output_csv)

    def extract_values(self):
        """
        Extracts raster values using the centroids of polygons defined in a GeoPackage file.
        The method reads the GeoPackage, calculates centroids, opens the TIFF file,
        extracts the raster values at these centroids, and saves the results to a CSV file.
        """
        logging.info(f'Starting raster value extraction...')
        try:
            # Read a GeoPackage containing polygons
            lagos_poly = gpd.read_file(self.gpkg_file)
            # Replace the geometry of each polygon with its centroid
            lagos_poly["geometry"] = lagos_poly.centroid

            # Open a raster file that contains a resampled tif file with lagos_bgrn
            with gw.open(self.tif_file) as src:
                logging.info(f'tiff file {self.tif_file} opened successfully.')
                # Extract raster values using the centroids of the polygons defined in 'lagos_poly'
                df = gw.extract(
                    src,
                    lagos_poly,
                    nodata=-9999,
                )
                logging.info('Data extraction from tiff file completed.')

                # Rename columns in the extracted DataFrame
                df.rename(columns={1: 'bgrn_1', 2: 'bgrn_2', 3: 'bgrn_3', 4: 'bgrn_4'}, inplace=True)

                # Select only the 'geometry' column and the BGRN band values from the DataFrame
                df = df[['geometry', 'bgrn_1', 'bgrn_2', 'bgrn_3', 'bgrn_4']]

                # Save the extracted data to a CSV file
                df.to_csv(self.output_csv, index=False)
                logging.info(f'BGRN CSV saved successfully to {self.output_csv}')

        except Exception as e:
            logging.error(f'Error during extraction: {e}')
