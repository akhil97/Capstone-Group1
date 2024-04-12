import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CSVMerger:
    def __init__(self, covariate_file, merged_contextual_feature_file, bgrn_file, output_file):
        """
        Initializes the CSVMerger with file paths for merging.

        Args:
        covariate_file (str): File path for the CSV containing the covariate data.
        merged_contextual_feature_file (str): File path for the CSV containing the contextual features data.
        bgrn_file (str): File path for the CSV containing BGRN band values.
        output_file (str): File path where the merged data will be saved as a new CSV file.
        """
        self.covariate_file = os.path.join(os.getcwd(), covariate_file)
        self.merged_contextual_feature_file = os.path.join(os.getcwd(), merged_contextual_feature_file)
        self.bgrn_file = os.path.join(os.getcwd(), bgrn_file)
        self.output_file = os.path.join(os.getcwd(), output_file)

    def merge_csvs_on_geometry(self):
        """
        Merges three CSV files based on a common 'geometry' column and saves the merged data to a new CSV file.

        The function reads the specified CSV files into pandas DataFrames, then merges them using
        pandas' merge function on the 'geometry' column. The merge is performed as an 'outer' join,
        ensuring that all entries from all tables are included in the result, with missing values filled with NaNs
        where no matching geometry is found. The merged DataFrame is then saved to the specified output file path.
        """
        logging.info('Starting the merging process.')
        try:
            # Load the data from the specified CSV files
            df_covariate = pd.read_csv(self.covariate_file)
            df_contextual_feature = pd.read_csv(self.merged_contextual_feature_file)
            df_bgrn = pd.read_csv(self.bgrn_file)

            # Merge the DataFrames on the 'geometry' column using an 'outer' join
            df_merged_1 = pd.merge(df_covariate, df_contextual_feature, on='geometry', how='outer')
            df_merged_final = pd.merge(df_merged_1, df_bgrn, on='geometry', how='outer')

            # Save the merged DataFrame to the specified output file
            df_merged_final.to_csv(self.output_file, index=False)
            logging.info(f'Merged all CSVs saved successfully to {self.output_file}. Merging process completed.')

        except Exception as e:
            logging.error(f'Error during merging process: {e}')
