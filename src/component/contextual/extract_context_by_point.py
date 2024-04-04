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
        self.lagos_poly = self.read_and_extract_polygons()

    def read_and_extract_polygons(self)
        # Read the geospatial polygons from the GeoPackage
        lagos_poly = gpd.read_file(self.gpkg_path)

        # Calculate the centroids of the polygons
        lagos_poly["geometry"] = lagos_poly.centroid

        return lagos_poly
        
    def get_tiff_files(self, base_dir):
        """
        Get TIFF files from subdirectories.
        
        Args:
            base_dir (str): Starting directory path.
        
        Returns:
            List of paths to TIFF files found within `base_dir` and its subdirectories.
        """
        tiff_files = []
        for dirpath, _, filenames in os.walk(base_dir):
            for filename in filenames:
                if filename.endswith('.tif'):
                    tiff_files.append(os.path.join(dirpath, filename))
        return tiff_files
        
    def process_tif(self, tif_file):
        """
        Processes a given TIFF file by extracting information based on a provided geospatial polygon,
        and saves the extracted information to a CSV file.

        Args:
        tif_file (str): The path to the TIFF file to be processed.
        """
        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        try: 
        # Open the TIFF file for reading
            with gw.open(tif_file) as src:
                # Extract data for the resampled contextual TIFF file within the provided polygon, handling nodata values
                df = gw.extract(src,
                                self.lagos_poly,
                                nodata=-9999)

                # Extract the feature name
                feature_name = os.path.splitext(os.path.basename(tif_file))[0]

                # Construct the output CSV file path
                output_csv_path = os.path.join(self.output_dir, f"{feature_name}_centroid.csv")

                # Save the extracted data to the CSV file
                df.to_csv(output_csv_path, index=False)
                
        except Exception as e:
            print(f"Error processing {tif_file}: {e}")

    def process_all_tifs(self):
        # Retrieve all TIFF file paths in the specified directory
        tif_files = self.get_tiff_files(self.tif_directory)

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.process_tif, tif_file) for tif_file in tif_files]

            for future in futures:
                future.result()
