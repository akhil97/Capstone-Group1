
import rasterio
import geopandas as gpd
import sys
import logging
from rasterio import features
from rasterio.enums import Resampling
from rasterio.features import rasterize
import numpy as np
import os
import matplotlib.pyplot as plt

#with rasterio.open('../../../Data/Lagos_Slum_reference.gpkg', mode="r") as src:
#    out_arr = src.read(1)
#    print(out_arr)
#    print(out_arr.shape)
def read_and_resample_raster(file_path, output_path, resampling_factor, resampling_method=Resampling.bilinear):
    """
       Load raster data and resample it.
       Args:
           input_tiff (str): Path to the raster file.
           resampling_factor (int): Factor by which to resample the raster.
       Returns:
           resampled_dataset: Resampled raster dataset.
    """
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

        df = gpd.read_file('../../../Data/Lagos_Slum_reference.gpkg')
        # lose a bit of resolution, but this is a fairly large file, and this is only an example.
        shape = 10, 10
        transform = rasterio.transform.from_bounds(*df['geometry'].total_bounds, *shape)
        rasterize_rivernet = rasterize(
            [(shape, 1) for shape in df['geometry']],
            out_shape=shape,
            transform=transform,
            fill=0,
            all_touched=True,
            dtype=rasterio.uint8)

        with rasterio.open(
                '../../../Data/rasterized-results.tif', 'w',
                driver='GTiff',
                dtype=rasterio.uint8,
                count=1,
                width=shape[0],
                height=shape[1],
                transform=transform
        ) as dst:
            dst.write(rasterize_rivernet, indexes=1)

        file_path = '../../../Data/rasterized-results.tif'
        output_path = '/home/ubuntu/Cap2024/train/lag_bgrn_resampled_file.tif'
        resampling_factor = 10  # Adjust as needed

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Process and resample the TIFF file
        read_and_resample_raster(file_path, output_path, resampling_factor)

    except Exception as e:
        logging.error(f"Error in main function: {e}")
        sys.exit(1)



