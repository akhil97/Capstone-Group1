import pandas as pd
import glob
import os

class CSVConcatenator:
    def __init__(self, input_dir, output_file, suffix='_centroid.csv'):
        """
        Initializes the CSVConcatenator object with the input directory, output file path,
        and the suffix to be removed from filenames when creating column names.

        Args:
            input_dir (str): Directory containing the CSV files to concatenate.
            output_file (str): Path where the concatenated CSV file will be saved.
            suffix (str): Suffix in the filenames to be removed. Defaults to '_centroid.csv'.
        """
        self.input_dir = input_dir
        self.output_file = output_file
        self.suffix = suffix

    def concat_csv_files(self):
        """
        Concatenates CSV files in the specified input directory and saves the merged DataFrame to the output file.
        Each CSV file must have a 'geometry' column and one additional column containing feature values.
        The name of the additional column is derived from the filename, excluding the specified suffix.
        """
        # Construct the pattern to match CSV files in the input directory
        file_pattern = os.path.join(self.input_dir, '*.csv')
        # Retrieve the list of all CSV files matching the pattern
        csv_files = glob.glob(file_pattern)

        # Initialize the merged DataFrame
        merged_df = None

        for file in csv_files:
            # Read the current CSV file into a DataFrame
            df = pd.read_csv(file)

            # Extract the feature name from the filename, excluding the specified suffix
            feature_name = os.path.basename(file).replace(self.suffix, '')
            # Keep only the 'geometry' column and the last column, renaming the last column to the extracted feature name
            df = df[['geometry', df.columns[-1]]].rename(columns={df.columns[-1]: feature_name})

            if merged_df is None:
                merged_df = df
            else:
                # Merge the current DataFrame with the merged DataFrame based on the 'geometry' column
                merged_df = pd.merge(merged_df, df, on='geometry', how='outer')

        # Save the merged DataFrame to a CSV file at the specified output path
        merged_df.to_csv(self.output_file, index=False)
