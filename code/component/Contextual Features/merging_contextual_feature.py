import pandas as pd
import glob
import os

def concat_context_csv(input_dir, output_file):
    file_pattern = os.path.join(input_dir, '*.csv')
    csv_files = glob.glob(file_pattern)

    merged_df = None

    for file in csv_files:
        df = pd.read_csv(file)

        feature_name = os.path.basename(file).replace('_centroid.csv', '')
        df = df[['geometry', df.columns[-1]]].rename(columns={df.columns[-1]: feature_name})

        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on='geometry', how='outer')

    merged_df.to_csv(output_file, index=False)

input_dir = '/home/ubuntu/Cap2024/context/contextual_features_extraction'
output_dir = '/home/ubuntu/Cap2024/context/merged_all_feature.csv'
concat_context_csv(input_dir, output_dir)