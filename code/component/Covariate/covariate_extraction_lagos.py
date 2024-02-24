import rasterio
import pandas as pd
import multiprocessing
from itertools import product

def process(row, src_path, num_bands):
    data_list = []
    with rasterio.open(src_path) as src:
        for col in range(src.width):
            pixel_values = []
            for band in range(1, num_bands + 1):
                value = src.read(band, window=((row, row + 1), (col, col + 1))).flatten()[0]
                if value != src.nodatavals[band - 1]:
                    pixel_values.append(value)
                else:
                    pixel_values.append(float('NaN'))

            lon, lat = src.xy(row, col)
            data_list.append([lon, lat] + pixel_values)
    return data_list

def main():
    tiff_path = "/home/ubuntu/Cap2024/covariate/lag_covariate_compilation_53bands_clip.tif"
    output_csv_path = "/home/ubuntu/Cap2024/covariate/Covariate_Features.csv"

    try:
        with rasterio.open(tiff_path) as src:
            num_bands = src.count
            pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

            results = pool.starmap(process, [(row, tiff_path, num_bands) for row in range(src.height)])
            pool.close()
            pool.join()

            # Flatten the list of results
            flat_results = [item for sublist in results for item in sublist]

            # Create a DataFrame
            data_df = pd.DataFrame(flat_results, columns=['Longitude', 'Latitude'] + [f'Band_{i + 1}' for i in range(num_bands)])
            print(f"Total number of data points extracted: {len(data_df)}")

            # Save the DataFrame to CSV
            data_df.to_csv(output_csv_path, index=False)

    except rasterio.errors.RasterioIOError as e:
        print(f"Error opening the TIFF file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()




