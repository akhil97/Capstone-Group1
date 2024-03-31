import pandas as pd

def merge_csvs_on_geometry(final_cvs_file, bgrn_file, output_file):
    """
        Merges an existing final CSV file (including contextual feature data and covariate data) with a new CSV file
        containing bgrn (e.g., Blue, Green, Red, Near-infrared) band values, based on matching 'geometry' values.
        The merged data is saved to a specified output CSV file.

        Args:
            final_csv_file (str): File path to the existing final CSV file containing geospatial data.
            bgrn_file (str): File path to the CSV file containing bgrn band values and their associated geometries.
            output_file (str): File path where the merged data should be saved as a new CSV file.
        """
    # Load the final CSV file and the bgrn values file into pandas DataFrames
    df_final_file = pd.read_csv(final_cvs_file)
    df_bgrn = pd.read_csv(bgrn_file)

    # Select only the 'geometry' column and the bgrn band values from the bgrn DataFrame
    df_bgrn = df_bgrn[['geometry', 'bgrn_1', 'bgrn_2', 'bgrn_3', 'bgrn_4']]


    # Merge the two DataFrames on the 'geometry' column using an outer join
    df_merged = pd.merge(df_final_file, df_bgrn, on='geometry', how='outer')

    # Save the merged DataFrame to the specified output CSV file
    df_merged.to_csv(output_file, index=False)

# Specify the file paths for the existing final dataset, the new bgrn values file, and the output file
df_final_file = '/home/ubuntu/Cap2024/combined_data/final_output.csv'
df_bgrn = '/home/ubuntu/Cap2024/raw_image/lagos_bgrn_resampled.csv'
output_file = '/home/ubuntu/Cap2024/combined_data/final_output_1.csv'

# Execute the merging function with the provided file paths
merge_csvs_on_geometry(df_final_file, df_bgrn, output_file)