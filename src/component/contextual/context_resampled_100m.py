import os
import rasterio
from rasterio.enums import Resampling
import logging
from concurrent.futures import ProcessPoolExecutor

class RasterResampler:
    def __init__(self, base_dir, resampling_factor, output_dir):
        self.base_dir = base_dir
        self.resampling_factor = resampling_factor
        self.output_dir = output_dir

    def read_and_resample_raster(self, file_path, resampling_method=Resampling.bilinear):
        try:
            with rasterio.open(file_path) as dataset:
                new_height = int(dataset.height * self.resampling_factor)
                new_width = int(dataset.width * self.resampling_factor)

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

                return resampled_data, dataset.count, dtype, dataset.crs, transform

        except Exception as e:
            logging.error(f'Error reading and resampling raster {file_path}: {e}')
            return None

    def get_tiff_files(self):
        tiff_files = []
        for dirpath, _, filenames in os.walk(self.base_dir):
            for filename in filenames:
                if filename.endswith('.tif'):
                    tiff_files.append(os.path.join(dirpath, filename))
        return tiff_files

    def process_file(self, file_path):
        try:
            result = self.read_and_resample_raster(file_path)
            if result:
                resampled_data, count, dtype, crs, transform = result
                output_file = os.path.join(self.output_dir, f'resampled_{os.path.basename(file_path)}')
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

    def process_tif(self):
        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)

            tiff_files = self.get_tiff_files()
            logging.info(f"Found {len(tiff_files)} TIFF files to process.")

            with ProcessPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(self.process_file, file_path): file_path for file_path in tiff_files}

                for future in futures:
                    file_path = futures[future]
                    try:
                        future.result()
                        logging.info(f"Completed processing of {file_path}")
                    except Exception as e:
                        logging.error(f"Error in processing file {file_path}: {e}")

        except Exception as e:
            logging.error(f"Error in main function: {e}")