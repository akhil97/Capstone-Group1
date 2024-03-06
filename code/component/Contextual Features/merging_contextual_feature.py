import os
import pandas as pd
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def merge_csv_files(directory, output_filename):
    try:
        # Dictionary to hold data from each CSV file with the filename as key
        data_dict = {}

        # Read the longitude and latitude from the first file to use as a base for merging
        first_file = next((f for f in os.listdir(directory) if f.endswith('.csv')), None)
        if first_file is None:
            logging.error("No CSV files found in the directory.")
            return

        base_df = pd.read_csv(os.path.join(directory, first_file))[['longitude', 'latitude']]

        # Iterate over files in the directory and read only the 'Raster Value' column
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                # Extract the name for the new column from the filename
                column_name = os.path.splitext(filename)[0]
                # Read the 'Raster Value' column and add it to the dictionary
                data_dict[column_name] = pd.read_csv(file_path)['Raster Value']

        # Concatenate all raster value columns along the columns axis
        raster_values_df = pd.concat(data_dict, axis=1)

        # Join the base_df with the raster values dataframe
        merged_df = base_df.join(raster_values_df)

        # Remove rows with any NaN value
        cleaned_df = merged_df.dropna()

        # Save the cleaned dataframe to a new CSV file
        cleaned_df.to_csv(output_filename, index=False)
        logging.info(f'Merged and cleaned files into {output_filename}')

    except Exception as e:
        logging.error(f"Error occurred: {e}")

if __name__ == '__main__':
    directory = '/home/ubuntu/Cap2024/context/contextual_features_extraction'
    output_filename = '/home/ubuntu/Cap2024/context/merged_contextual_features.csv'
    merge_csv_files(directory, output_filename)

