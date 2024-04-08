import os
import sys

sys.path.append('/home/ubuntu/Cap2024')

from src.component.covariate import extract_by_point

from src.component.contextual import extract_context_by_point
from src.component.contextual import merging_contextual_feature

from src.component.rawimageproc import coordinate_pixel_extraction

from src.component.combinedata import combined_data_1


if __name__ == '__main__':
    #Step-1
    # Define file paths
    poly_file = "/home/ubuntu/Cap2024/CapstoneDataset2024/Capstone_2024/Reference/Deprived_Areas/Lagos_Slum_reference.gpkg"
    raster_file = "/home/ubuntu/Cap2024/CapstoneDataset2024/Capstone_2024/Dataset/Lagos/lagos_covariate_feature_53/lag_covariate_compilation_53bands.tif"
    output_file = "/home/ubuntu/Cap2024/covariate/lagos_centroid.csv"

    # Create an instance of the Extractor class
    extractor = extract_by_point.Extractor(poly_file, raster_file, output_file)

    # Call the extract_data() method
    extractor.extract_data()

    #Step-2
    gpkg_path = '/home/ubuntu/Cap2024/CapstoneDataset2024/Capstone_2024/Reference/Deprived_Areas/100mGrid_Lagos.gpkg'
    tif_directory = '/home/ubuntu/Cap2024/context/lagos_contextual_10m'
    output_dir = '/home/ubuntu/Cap2024/context/contextual_features_extraction_1'
    processor = extract_context_by_point.TIFFProcessor(gpkg_path, tif_directory, output_dir)
    processor.process_all_tifs()

    #Step-3
    input_dir = '/home/ubuntu/Cap2024/context/contextual_features_extraction_1'
    output_file = '/home/ubuntu/Cap2024/context/merged_all_feature_1.csv'
    concatenator = merging_contextual_feature.CSVConcatenator(input_dir, output_file)
    concatenator.concat_csv_files()

    #Step-4
    gpkg_file = "/home/ubuntu/Cap2024/CapstoneDataset2024/Capstone_2024/Reference/Deprived_Areas/100mGrid_Lagos.gpkg"
    tif_file = "/home/ubuntu/Cap2024/raw_image/lag_bgrn.tif"
    output_csv = "/home/ubuntu/Cap2024/raw_image/lagos_bgrn.csv"
    extractor = coordinate_pixel_extraction.ExtractRasterValues(gpkg_file, tif_file, output_csv)
    extractor.extract_values()

    #Step-5
    covariate_file = '/home/ubuntu/Cap2024/covariate/lagos_centroid.csv'
    merged_contextual_feature_file = '/home/ubuntu/Cap2024/context/merged_all_feature_1.csv'
    bgrn_file = '/home/ubuntu/Cap2024/raw_image/lagos_bgrn.csv'
    output_file = '/home/ubuntu/Cap2024/combined_data/final_output_lagos.csv'
    merger = combined_data_1.CSVMerger(covariate_file, merged_contextual_feature_file, bgrn_file, output_file)
    merger.merge_csvs_on_geometry()
