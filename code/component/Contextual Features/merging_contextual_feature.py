import pandas as pd
import glob
import os

def concat_context_csv(input_dir, output_file):
    """
    Concatenates multiple CSV files located in a specified directory into a single CSV file.
    Each CSV file is expected to have a 'geometry' column and one additional column containing feature values.
    The name of the additional column is derived from the filename and is used as the feature name in the merged DataFrame.

    Args:
    input_dir (str): The directory containing the CSV files to concatenate.
    output_file (str): The path where the concatenated CSV file will be saved.

    Returns:
    None: The function does not return a value but writes the merged DataFrame to a CSV file.
    """

    # Construct the pattern to match CSV files in the input directory
    file_pattern = os.path.join(input_dir, '*.csv')
    
    # Retrieve the list of all CSV files matching the pattern
    csv_files = glob.glob(file_pattern)

    # Initialize the merged DataFrame
    merged_df = None

    # Iterate over each file in the list of CSV files
    for file in csv_files:
        # Read the current CSV file into a DataFrame
        df = pd.read_csv(file)

        # Extract the feature name from the filename (excluding '_centroid.csv')
        feature_name = os.path.basename(file).replace('_centroid.csv', '')
        
        # Keep only the 'geometry' column and the last column, renaming the last column to the extracted feature name
        df = df[['geometry', df.columns[-1]]].rename(columns={df.columns[-1]: feature_name})

        # If merged_df is None, assign df to merged_df
        if merged_df is None:
            merged_df = df
        else:
            # Merge the current DataFrame with the merged DataFrame based on the 'geometry' column
            merged_df = pd.merge(merged_df, df, on='geometry', how='outer')
    # Save the merged DataFrame to a CSV file at the specified output path
    merged_df.to_csv(output_file, index=False)

# Define the input directory containing the CSV files
input_dir = '/home/ubuntu/Cap2024/context/contextual_features_extraction'

# Define the path to the output file where the concatenated CSV will be saved
output_dir = '/home/ubuntu/Cap2024/context/merged_all_feature.csv'

# Call the function to concatenate the CSV files and save them to the specified output file
concat_context_csv(input_dir, output_dir)
