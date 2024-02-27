import sys
import os
import rasterio
import pandas as pd
import numpy as np
import logging

def extract_coordinates_and_labels(file_path):
    """
    Extracts coordinates and labels from a TIFF file.
    Args:
        file_path (str): Path to the TIFF file.
    Returns:
        DataFrame: Contains longitude, latitude, and labels.
    """
    try:
        with rasterio.open(file_path) as dataset:
            val = dataset.read(1)
            no_data = dataset.nodata

            data = [(dataset.xy(x, y)[0], dataset.xy(x, y)[1], val[x, y])
                    for x, y in np.ndindex(val.shape) if val[x, y] != no_data]

            lon = [i[0] for i in data]
            lat = [i[1] for i in data]
            labels = [i[2] for i in data]
            df = pd.DataFrame({"longitude": lon, "latitude": lat, "label": labels})

            return df

    except Exception as e:
        logging.error(f'Error extracting coordinates and labels from {file_path}: {e}')
        return None

if __name__ == "__main__":
    try:
        file_path = '/home/ubuntu/Cap2024/train/lag_bgrn_resampled_file.tif'
        output_file = '/home/ubuntu/Cap2024/train/extracted_data.csv'

        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Extract coordinates and labels from the TIFF file
        df = extract_coordinates_and_labels(file_path)
        if df is not None:
            df.to_csv(output_file, index=False)
            logging.info(f"Data extracted and saved to {output_file}")

    except Exception as e:
        logging.error(f"Error in main function: {e}")
        sys.exit(1)
