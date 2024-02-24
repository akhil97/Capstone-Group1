import os
import numpy as np
import rasterio as rio
import pandas as pd
import logging
import multiprocess
from concurrent.futures import ProcessPoolExecutor

# Get the number of CPU cores
max_workers = multiprocess.cpu_count()

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get coordinates from a raster file
def get_raster_coordinates(file_path):
    try:
        with rio.open(file_path) as src:
            array = src.read(1)
            rows, cols = np.indices(array.shape)
            xs, ys = rio.transform.xy(src.transform, rows.flatten(), cols.flatten(), offset='center')
            return xs, ys
    except Exception as e:
        logging.error(f"Error in getting raster coordinates from {file_path}: {e}")
        return None, None

# Function to get TIFF file paths from a directory
def get_tiff_files(base_dir):
    tiff_files = []
    for dirpath, _, filenames in os.walk(base_dir):
        for filename in filenames:
            if filename.endswith('.tif'):
                tiff_files.append(os.path.join(dirpath, filename))
    return tiff_files

# Function to adjust coordinates and create tuples
def adjust_coordinates_and_create_tuples(xs, ys):
    # 1. Approximate step size (value = 0.0009) for 100 meters at the equator
    # 2. By multiplying this step size by 10, the function effectively shifts each longitude coordinate westward by
    # approximately 1000 meters and each latitude coordinate northward by approximately 1000 meters.
    xs_adjusted = [x - 10 * 0.0009 for x in xs]
    ys_adjusted = [y + 10 * 0.0009 for y in ys]
    return list(zip(xs_adjusted, ys_adjusted))

# Function to process a single TIFF file
def process_tiff_file(tiff_file, output_dir):
    try:
        xs, ys = get_raster_coordinates(tiff_file)
        if xs is None or ys is None:
            return

        sample_coords = adjust_coordinates_and_create_tuples(xs, ys)

        with rio.open(tiff_file) as src:
            raster_values = [x[0] for x in src.sample(sample_coords)]
            data_tuples = list(zip(sample_coords, raster_values))
            adjusted_data = pd.DataFrame(
                [(lon, lat, val) for ((lon, lat), val) in data_tuples],
                columns=['longitude', 'latitude', 'Raster Value'])

            output_csv_filename = os.path.splitext(os.path.basename(tiff_file))[0] + '.csv'
            output_csv_path = os.path.join(output_dir, output_csv_filename)
            adjusted_data.to_csv(output_csv_path, index=False)
            logging.info(f"Processed {tiff_file} and saved data as {output_csv_filename}")

    except Exception as e:
        logging.error(f"Error processing {tiff_file}: {e}")

# Main function to process TIFF files and generate CSVs
def main(base_dir, output_dir):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        tiff_files = get_tiff_files(base_dir)
        logging.info(f"Found {len(tiff_files)} TIFF files to process.")

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_tiff_file, tiff_file, output_dir) for tiff_file in tiff_files]
            for future in futures:
                future.result()
    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == '__main__':
    base_dir = '/home/ubuntu/Cap2024/context/resampled_data'
    output_dir = '/home/ubuntu/Cap2024/context/contextual_features_extraction'
    main(base_dir, output_dir)
