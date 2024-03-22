import pandas as pd

def merge_cvs_on_geometry(merged_contextual_feature_file, covariate_file, output_file):
    df_contextual_feature = pd.read_csv(merged_contextual_feature_file)
    df_covariate = pd.read_csv(covariate_file)

    df_merged = pd.merge(df_covariate, df_contextual_feature, on='geometry', how='outer')

    df_merged.to_csv(output_file, index=False)

df_contextual_feature = '/home/ubuntu/Cap2024/context/merged_all_feature.csv'
df_covariate = '/home/ubuntu/Cap2024/covariate/lagos_centroid.csv'
output_file = '/home/ubuntu/Cap2024/combined_data/final_output.csv'

merge_cvs_on_geometry(df_contextual_feature,df_covariate, output_file)