import sys
import os
import numpy as np
import rioxarray
from osgeo import gdal, ogr
import rasterio as rio
import logging
from concurrent.futures import ProcessPoolExecutor

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_and_resample_raster(file_path, resampling_factor):
    """
    Load raster data and resample it.
    Args:
        file_path (str): Path to the raster file.
        resampling_factor (int): Factor by which to resample the raster.
    Returns:
        resampled_dataset: Resampled raster dataset.
    """
    try:
        with rioxarray.open_rasterio(file_path) as dataset:
            resampled_dataset = dataset.rio.reproject(
                dataset.rio.crs,
                resolution=(resampling_factor, resampling_factor)
            )
            return resampled_dataset
    except Exception as e:
        logging.error(f'Error reading and resampling raster {file_path}: {e}')
        raise

def get_tiff_files(base_dir):
    """
    Get TIFF files from subdirectories.
    Args:
        base_dir (str): Base directory to search for TIFF files.
    Returns:
        tiff_files (list): List of paths to TIFF files.
    """
    tiff_files = []
    for dirpath, _, filenames in os.walk(base_dir):
        for filename in filenames:
            if filename.endswith('.tif'):
                tiff_files.append(os.path.join(dirpath, filename))
    return tiff_files

def main(base_dir, resampling_factor, output_dir):
    """
    Main function to process TIFF files.
    Args:
        base_dir (str): Base directory containing TIFF files.
        resampling_factor (int): Factor by which to resample the raster.
        output_dir (str): Directory where the output files will be saved.
    """
    try:
        # Ensure output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        tiff_files = get_tiff_files(base_dir)
        logging.info(f"Found {len(tiff_files)} TIFF files to process.")

        with ProcessPoolExecutor() as executor:
            futures = []
            for i, tiff_file in enumerate(tiff_files):
                logging.info(f"Submitting file {tiff_file} for resampling.")
                future = executor.submit(read_and_resample_raster, tiff_file, resampling_factor)
                futures.append(future)

            for i, future in enumerate(futures):
                try:
                    resampled_data = future.result()
                    output_file = os.path.join(output_dir, f'resampled_{i}.tif')
                    resampled_data.rio.to_raster(output_file)
                    logging.info(f"Saved resampled data to {output_file}")

                except Exception as e:
                    logging.error(f"Error in processing file {tiff_files[i]}: {e}")

    except Exception as e:
        logging.error(f"Error in main function: {e}")
        sys.exit(1)

if __name__ == '__main__':
    base_dir = '/home/ubuntu/Cap2024/context/lagos_contextual_10m'
    resampling_factor = 100
    output_dir = '/home/ubuntu/Cap2024/context/resampled_data'
    main(base_dir, resampling_factor, output_dir)






