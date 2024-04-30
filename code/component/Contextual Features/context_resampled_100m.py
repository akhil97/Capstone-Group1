import sys
import os
import rasterio
from rasterio.enums import Resampling
import logging
from concurrent.futures import ProcessPoolExecutor

# Setup basic logging to display messages with time, log level, and message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_and_resample_raster(file_path, resampling_factor, resampling_method=Resampling.bilinear):
    """
    Load raster data and resample it.
    Args:
        file_path (str): Path to the raster file.
        resampling_factor (float): Factor by which to resample the raster.
        resampling_method (Resampling): Method used for resampling.
    Returns:
        Tuple of resampled data and its transformation.
    """
    try:
        with rasterio.open(file_path) as dataset:
            # Calculate new dimensions based on the resampling factor
            new_height = int(dataset.height * resampling_factor)
            new_width = int(dataset.width * resampling_factor)

            # Resample the dataset to the new dimensions
            resampled_data = dataset.read(
                out_shape=(
                    dataset.count,
                    new_height,
                    new_width
                ),
                resampling=resampling_method
            )
            # Get the data type of the resampled data
            dtype = resampled_data.dtype

            # Calculate new transform object for the resampled data
            transform = dataset.transform * dataset.transform.scale(
                (dataset.width / new_width),
                (dataset.height / new_height)
            )

            return resampled_data, dataset.count, dtype, dataset.crs, transform

    except Exception as e:
        logging.error(f'Error reading and resampling raster {file_path}: {e}')
        return None

def get_tiff_files(base_dir):
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

def process_file(file_path, resampling_factor, output_dir):
    """
    Process a single file.
    Args:
        file_path (str): Path to the input TIFF file.
        resampling_factor (float): Factor to resample the TIFF file.
        output_dir (str): Directory where resampled TIFFs will be saved.
    """
    try:
        result = read_and_resample_raster(file_path, resampling_factor)
        if result:
            # Unpack the result to individual variables
            resampled_data, count, dtype, crs, transform = result
            output_file = os.path.join(output_dir, f'resampled_{os.path.basename(file_path)}')

            # Save the resampled raster to a new file
            with rasterio.open(
                output_file,
                'w',
                driver='GTiff',
                height=resampled_data.shape[1],
                width=resampled_data.shape[2],
                count=count,
                dtype=dtype,
                crs=crs,
                transform=transform,
            ) as dst:
                dst.write(resampled_data)
            logging.info(f"Saved resampled data to {output_file}")
    except Exception as e:
        logging.error(f"Error in processing file {file_path}: {e}")

def main(base_dir, resampling_factor, output_dir):
    """
    Main function to process TIFF files.
    Args:
        base_dir (str): Directory containing original TIFF files.
        resampling_factor (float): Factor to resample each TIFF file.
        output_dir (str): Directory to save resampled TIFF files.
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Get all TIFF files in the base directory
        tiff_files = get_tiff_files(base_dir)
        logging.info(f"Found {len(tiff_files)} TIFF files to process.")

        # Use a ProcessPoolExecutor to process files in parallel
        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(process_file, file_path, resampling_factor, output_dir): file_path for file_path in tiff_files}

            for future in futures:
                file_path = futures[future]
                try:
                    future.result()
                    logging.info(f"Completed processing of {file_path}")
                except Exception as e:
                    logging.error(f"Error in processing file {file_path}: {e}")

    except Exception as e:
        logging.error(f"Error in main function: {e}")
        sys.exit(1)

if __name__ == '__main__':
    base_dir = '/home/ubuntu/Cap2024/context/lagos_contextual_10m'
    resampling_factor = 0.1 # Define the resampling factor, here set to reduce the resolution to 10%
    output_dir = '/home/ubuntu/Cap2024/context/resampled_data'
    main(base_dir, resampling_factor, output_dir)



