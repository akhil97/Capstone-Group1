import pandas as pd


class CSVMerger:
    def __init__(self, final_csv_file, bgrn_file, output_file):
        self.final_csv_file = final_csv_file
        self.bgrn_file = bgrn_file
        self.output_file = output_file

    def merge_csvs_on_geometry(self):
        """
        Merges an existing final CSV file (including contextual feature data and covariate data) with a new CSV file
        containing bgrn (e.g., Blue, Green, Red, Near-infrared) band values, based on matching 'geometry' values.
        The merged data is saved to a specified output CSV file.
        """
        # Load the final CSV file and the bgrn values file into pandas DataFrames
        df_final_file = pd.read_csv(self.final_csv_file)
        df_bgrn = pd.read_csv(self.bgrn_file)

        # Select only the 'geometry' column and the bgrn band values from the bgrn DataFrame
        df_bgrn = df_bgrn[['geometry', 'bgrn_1', 'bgrn_2', 'bgrn_3', 'bgrn_4']]

        # Merge the two DataFrames on the 'geometry' column using an outer join
        df_merged = pd.merge(df_final_file, df_bgrn, on='geometry', how='outer')

        # Save the merged DataFrame to the specified output CSV file
        df_merged.to_csv(self.output_file, index=False)