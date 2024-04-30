import os
import sys
import logging
import rasterio
from rasterio.enums import Resampling
from concurrent.futures import ProcessPoolExecutor

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TIFFResampler:
    def __init__(self, input_dir, output_dir, resampling_factor=0.1, resampling_method=Resampling.bilinear):
        """
        Initialize the TIFFResampler with paths and parameters.

        Args:
            input_dir (str): Directory containing original TIFF files.
            output_dir (str): Directory to save resampled TIFF files.
            resampling_factor (float): Factor to resample each TIFF file, multiply by 0.1 to reduce the resolution to 10%.
            resampling_method (Resampling): Method used for resampling.
        """
        self.input_dir = os.path.join(os.getcwd(), input_dir)
        self.output_dir = os.path.join(os.getcwd(), output_dir)
        self.resampling_factor = resampling_factor
        self.resampling_method = resampling_method

        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def get_tiff_files(self):
        """
        Get TIFF files from subdirectories.
        Returns:
            List of paths to TIFF files found within the base directory and its subdirectories.
        """
        tiff_files = []
        for dirpath, _, filenames in os.walk(self.input_dir):
            for filename in filenames:
                if filename.endswith('.tif'):
                    tiff_files.append(os.path.join(dirpath, filename))
        return tiff_files

    def read_and_resample_raster(self, file_path):
        """
        Load raster data and resample it.
        Args:
            file_path (str): Path to the raster file.
        Returns:
            Tuple of resampled data and its transformation, or None on failure.
        """
        try:
            with rasterio.open(file_path) as dataset:
                # Calculate new dimensions based on the resampling factor
                new_height = int(dataset.height * self.resampling_factor)
                new_width = int(dataset.width * self.resampling_factor)

                # Resample the dataset
                resampled_data = dataset.read(
                    out_shape=(dataset.count, new_height, new_width),
                    resampling=self.resampling_method
                )

                # Calculate new transform
                transform = dataset.transform * dataset.transform.scale(
                    (dataset.width / new_width),
                    (dataset.height / new_height)
                )

                return resampled_data, dataset.count, resampled_data.dtype, dataset.crs, transform
        except Exception as e:
            logging.error(f'Error reading and resampling raster {file_path}: {e}')
            return None

    def process_file(self, file_path):
        """
        Process a single file by resampling and saving it.
        Args:
            file_path (str): Path to the input TIFF file.
        """
        result = self.read_and_resample_raster(file_path)
        if result:
            resampled_data, count, dtype, crs, transform = result
            output_file = os.path.join(self.output_dir, f'resampled_{os.path.basename(file_path)}')

            # Save the resampled raster
            with rasterio.open(output_file,
                               'w',
                               driver='GTiff',
                               height=resampled_data.shape[1],
                               width=resampled_data.shape[2],
                               count=count,
                               dtype=dtype,
                               crs=crs,
                               transform=transform) as dst:
                dst.write(resampled_data)
            logging.info(f"Saved resampled data to {output_file}")

    def process_all_files(self):
        """
        Process all TIFF files in parallel using ProcessPoolExecutor.
        """
        tiff_files = self.get_tiff_files()
        logging.info(f"Found {len(tiff_files)} TIFF files to process.")

        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(self.process_file, file_path) for file_path in tiff_files]

            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error in processing a file: {e}")
