import sys
import os
import geopandas as gpd
sys.path.append('/home/ubuntu/Capstone/Capstone-Group1/')
from src.component.covariate import extract_by_point

#from src.component.contextual import context_resampled_100m
from src.component.contextual import extract_context_by_point
from src.component.contextual import merging_contextual_feature

#from src.component.rawimageproc import resample
from src.component.rawimageproc import coordinate_pixel_extraction

from src.component.combinedata import combined_data_1
from src.component.combinedata import combined_data_2

if __name__ == '__main__':
    #Step-1
    # Define file paths
    poly_file = "100mGrid_Lagos.gpkg"
    raster_file = "lag_covariate_compilation_53bands.tif"
    output_file = "lagos_centroid.csv"

    # Create an instance of the Extractor class
    extractor = extract_by_point.Extractor(poly_file, raster_file, output_file)

    # Call the extract_data() method
    extractor.extract_data()

    #Step-2
    processor = extract_context_by_point.TIFFProcessor(
    gpkg_path='/home/ubuntu/Cap2024/CapstoneDataset2024/Capstone_2024/Reference/Deprived_Areas/100mGrid_Lagos.gpkg',
    tif_directory='/home/ubuntu/Cap2024/context/resampled_data',
    output_dir='/home/ubuntu/Cap2024/context/contextual_features_extraction'
    )

    # Process all TIFF files
    processor.process_all_tifs()

    #Step-3
    # Define the input directory containing the CSV files
    input_dir = '/home/ubuntu/Cap2024/context/contextual_features_extraction'

    # Define the path to the output file where the concatenated CSV will be saved
    output_file = '/home/ubuntu/Cap2024/context/merged_all_feature.csv'

    # Create an instance of ConcatenateCSV
    concatenator = merging_contextual_feature.ConcatenateCSV(input_dir, output_file)

    # Call the concatenate method to concatenate the CSV files and save them to the specified output file
    concatenator.concatenate()

    #Step-4
    extractor = coordinate_pixel_extraction.ExtractRasterValues(
        gpkg_file="100mGrid_Lagos.gpkg",
        tif_file="lag_bgrn_resampled_file.tif",
        output_csv="lagos_bgrn_resampled.csv"
    )
    extractor.extract_values()

    #Step-5
    # Define file paths for the contextual feature data, covariate data, and the output file
    df_contextual_feature = '/home/ubuntu/Cap2024/context/merged_all_feature.csv'
    df_covariate = '/home/ubuntu/Cap2024/covariate/lagos_centroid.csv'
    output_file = '/home/ubuntu/Cap2024/combined_data/final_output.csv'

    # Instantiate the CSVMerger class and execute the merge function
    csv_merger = combined_data_1.CSVMerger(df_contextual_feature, df_covariate, output_file)
    csv_merger.merge_csvs_on_geometry()

    #Step-6
    # Specify the file paths for the existing final dataset, the new bgrn values file, and the output file
    final_csv_file = '/home/ubuntu/Cap2024/combined_data/final_output.csv'
    bgrn_file = '/home/ubuntu/Cap2024/raw_image/lagos_bgrn_resampled.csv'
    output_file = '/home/ubuntu/Cap2024/combined_data/final_output_1.csv'

    # Create an instance of the CSVMerger class and call the merge_csvs_on_geometry method
    csv_merger = combined_data_2.CSVMerger(final_csv_file, bgrn_file, output_file)
    csv_merger.merge_csvs_on_geometry()












