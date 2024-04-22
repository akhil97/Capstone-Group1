import os
import sys
import rasterio
from rasterio.enums import Resampling
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RasterResampler:
    def __init__(self, file_path, output_path, resampling_factor=0.1, resampling_method=Resampling.bilinear):
        """
        Initialize the RasterResampler with parameters for processing.

        Args:
            file_path (str): Path to the original raster file.
            output_path (str): Path where the resampled raster will be saved.
            resampling_factor (float): Factor by which the raster's resolution is changed.
            resampling_method (Resampling): Method used for resampling.
        """
        self.file_path = os.path.join(os.getcwd(), file_path)
        self.output_path = os.path.join(os.getcwd(), output_path)
        self.resampling_factor = resampling_factor
        self.resampling_method = resampling_method

    def resample_bgrn_raster(self):
        """
        Read a raster file, resample it, and save the resampled raster to a new file.
        """
        try:
            with rasterio.open(self.file_path) as dataset:
                # Calculate new dimensions
                new_height = int(dataset.height * self.resampling_factor)
                new_width = int(dataset.width * self.resampling_factor)

                # Resample the raster to the new dimensions
                resampled_data = dataset.read(
                    out_shape=(dataset.count,
                               new_height,
                               new_width),
                    resampling=self.resampling_method
                )

                # Get data type of the resampled raster
                dtype = resampled_data.dtype

                # Calculate the new transformation for the resampled raster
                transform = dataset.transform * dataset.transform.scale(
                    (dataset.width / new_width),
                    (dataset.height / new_height)
                )

                # Ensure output directory exists
                os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

                # Save the resampled raster to a new file
                with rasterio.open(
                        self.output_path,
                        'w',
                        driver='GTiff',
                        height=new_height,
                        width=new_width,
                        count=dataset.count,
                        dtype=dtype,
                        crs=dataset.crs,
                        transform=transform,
                ) as dst:
                    dst.write(resampled_data)

                logging.info(f'Resampled file saved to {self.output_path}')

        except Exception as e:
            logging.error(f'Error reading and resampling raster {self.file_path}: {e}')
