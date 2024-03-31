import pandas as pd

def merge_csvs_on_geometry(merged_contextual_feature_file, covariate_file, output_file):
    """
        Merges two CSV files based on a common 'geometry' column and saves the merged data to a new CSV file.

        Args:
            merged_contextual_feature_file (str): File path for the CSV containing the contextual features data.
            covariate_file (str): File path for the CSV containing the covariate data.
            output_file (str): File path where the merged data will be saved as a new CSV file.

        The function reads the two specified CSV files into pandas DataFrames, then merges them using
        pandas' merge function on the 'geometry' column. The merge is performed as an 'outer' join,
        ensuring that all entries from both tables are included in the result, with missing values filled with NaNs
        where no matching geometry is found. The merged DataFrame is then saved to the specified output file path.
        """
    # Load the contextual features and covariate data from their respective CSV files
    df_contextual_feature = pd.read_csv(merged_contextual_feature_file)
    df_covariate = pd.read_csv(covariate_file)

    # Merge the two DataFrames on the 'geometry' column using an 'outer' join
    df_merged_1 = pd.merge(df_covariate, df_contextual_feature, on='geometry', how='outer')
    
    # Save the merged DataFrame to a new CSV file
    df_merged_1.to_csv(output_file, index=False)

# Define file paths for the contextual feature data, covariate data, and the output file
df_contextual_feature = '/home/ubuntu/Cap2024/context/merged_all_feature.csv'
df_covariate = '/home/ubuntu/Cap2024/covariate/lagos_centroid.csv'
output_file = '/home/ubuntu/Cap2024/combined_data/final_output.csv'

# Execute the merge function with the specified file paths
merge_csvs_on_geometry(df_contextual_feature, df_covariate, output_file)
