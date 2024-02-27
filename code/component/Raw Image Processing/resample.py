import sys
import os
import rasterio
from rasterio.enums import Resampling
import logging

def read_and_resample_raster(file_path, output_path, resampling_factor, resampling_method=Resampling.bilinear):
    try:
        with rasterio.open(file_path) as dataset:
            new_height = int(dataset.height * resampling_factor)
            new_width = int(dataset.width * resampling_factor)

            resampled_data = dataset.read(
                out_shape=(
                    dataset.count,
                    new_height,
                    new_width
                ),
                resampling=resampling_method
            )

            dtype = resampled_data.dtype

            transform = dataset.transform * dataset.transform.scale(
                (dataset.width / new_width),
                (dataset.height / new_height)
            )

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

if __name__ == "__main__":
    try:
        file_path = '/home/ubuntu/Cap2024/train/lag_bgrn.tif'
        output_path = '/home/ubuntu/Cap2024/train/lag_bgrn_resampled_file.tif'
        resampling_factor = 0.1  # Adjust as needed

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Process and resample the TIFF file
        read_and_resample_raster(file_path, output_path, resampling_factor)

    except Exception as e:
        logging.error(f"Error in main function: {e}")
        sys.exit(1)
