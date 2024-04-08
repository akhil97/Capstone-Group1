import geopandas as gpd
import geowombat as gw
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExtractRasterValues:
    def __init__(self, gpkg_file, tif_file, output_csv):
        self.gpkg_file = gpkg_file
        self.tif_file = tif_file
        self.output_csv = output_csv

    def extract_values(self):
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

                # Save the extracted data to a CSV file
                df.to_csv(self.output_csv, index=False)
                logging.info(f'BGRN CSV saved successfully to {self.output_csv}')

        except Exception as e:
            logging.error(f'Error during extraction: {e}')