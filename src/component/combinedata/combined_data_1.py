import pandas as pd

class CSVMerger:
    def __init__(self, merged_contextual_feature_file, covariate_file, output_file):
        self.merged_contextual_feature_file = merged_contextual_feature_file
        self.covariate_file = covariate_file
        self.output_file = output_file

    def merge_csvs_on_geometry(self):
        """
        Merges two CSV files based on a common 'geometry' column and saves the merged data to a new CSV file.

        The function reads the two specified CSV files into pandas DataFrames, then merges them using
        pandas' merge function on the 'geometry' column. The merge is performed as an 'outer' join,
        ensuring that all entries from both tables are included in the result, with missing values filled with NaNs
        where no matching geometry is found. The merged DataFrame is then saved to the specified output file path.
        """
        # Load the contextual features and covariate data from their respective CSV files
        df_contextual_feature = pd.read_csv(self.merged_contextual_feature_file)
        df_covariate = pd.read_csv(self.covariate_file)

        # Merge the two DataFrames on the 'geometry' column using an 'outer' join
        df_merged = pd.merge(df_covariate, df_contextual_feature, on='geometry', how='outer')

        # Save the merged DataFrame to a new CSV file
        df_merged.to_csv(self.output_file, index=False)