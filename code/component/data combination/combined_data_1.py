import pandas as pd

def merge_csvs_on_geometry(covariate_file, merged_contextual_feature_file, bgrn_file, output_file):
    """
        Merges three CSV files based on a common 'geometry' column and saves the merged data to a new CSV file.

        Args:
            merged_contextual_feature_file (str): File path for the CSV containing the contextual features data.
            covariate_file (str): File path for the CSV containing the covariate data and slum lables.
            bgrn_file (str): File path for the CSV containing four bgrn data.
            output_file (str): File path where the merged data will be saved as a new CSV file.

        The function reads the three specified CSV files into pandas DataFrames, then merges them using
        pandas' merge function on the 'geometry' column. The merge is performed as an 'outer' join,
        ensuring that all entries from both tables are included in the result, with missing values filled with NaNs
        where no matching geometry is found. The merged DataFrame is then saved to the specified output file path.
        """
    # Load the contextual features and covariate data from their respective CSV files
    df_covariate = pd.read_csv(covariate_file)
    df_contextual_feature = pd.read_csv(merged_contextual_feature_file)
    df_bgrn = pd.read_csv(bgrn_file)

    # Select only the 'geometry' column and the bgrn band values from the bgrn DataFrame
    df_bgrn = df_bgrn[['geometry', 'bgrn_1', 'bgrn_2', 'bgrn_3', 'bgrn_4']]

    # Merge the two DataFrames on the 'geometry' column using an 'outer' join
    df_merged_1 = pd.merge(df_covariate, df_contextual_feature, on='geometry', how='outer')
    df_merged_final = pd.merge(df_merged_1, df_bgrn, on='geometry', how='outer')

    # Save the merged DataFrame to a new CSV file
    df_merged_final.to_csv(output_file, index=False)

# Define file paths for the contextual feature data, covariate data, and the output file
df_covariate = '/home/ubuntu/Cap2024/covariate/lagos_centroid.csv'
df_contextual_feature = '/home/ubuntu/Cap2024/context/merged_all_feature_1.csv'
df_bgrn = '/home/ubuntu/Cap2024/raw_image/lagos_bgrn.csv'
output_file = '/home/ubuntu/Cap2024/combined_data/final_output_lagos.csv'


# Execute the merge function with the specified file paths
merge_csvs_on_geometry(df_covariate, df_contextual_feature, df_bgrn, output_file)
