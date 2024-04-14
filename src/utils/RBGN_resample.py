import sys
import os
import rasterio
from rasterio.enums import Resampling
import logging

def read_and_resample_raster(file_path, output_path, resampling_factor, resampling_method=Resampling.bilinear):
    """
        Read a raster file, resample it, and save the resampled raster to a new file.

        Args:
            file_path (str): Path to the original raster file.
            output_path (str): Path where the resampled raster will be saved.
            resampling_factor (float): Factor by which the raster's resolution is changed.
            resampling_method (Resampling): Method used for resampling. Default is bilinear interpolation.

        The function opens the original raster file, calculates the new dimensions based on the resampling factor,
        and uses these dimensions to resample the raster data. The resampled raster is then saved to a new file at the
        specified output path.
        """
    try:
        with rasterio.open(file_path) as dataset:
            # Calculate new dimensions
            new_height = int(dataset.height * resampling_factor)
            new_width = int(dataset.width * resampling_factor)

            # Resample the raster to the new dimensions
            resampled_data = dataset.read(
                out_shape=(
                    dataset.count,
                    new_height,
                    new_width
                ),
                resampling=resampling_method
            )

            # Get data type of the resampled raster
            dtype = resampled_data.dtype

            # Calculate the new transformation for the resampled raster
            transform = dataset.transform * dataset.transform.scale(
                (dataset.width / new_width),
                (dataset.height / new_height)
            )
            # Save the resampled raster to a new file
            with rasterio.open(
                output_path,
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

            logging.info(f'Resampled file saved to {output_path}')

    except Exception as e:
        logging.error(f'Error reading and resampling raster {file_path}: {e}')

