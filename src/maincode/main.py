import os
import sys

project_path = '/home/ubuntu/Cap2024'
sys.path.append(project_path)

from src.component.covariate import extract_by_point

from src.component.contextual import extract_context_by_point
from src.component.contextual import merging_contextual_feature

from src.component.rawimageproc import coordinate_pixel_extraction

from src.component.combinedata import combined_data_1


if __name__ == '__main__':
    # Define base directory
    base_dir = project_path

    # Step-1
    # Define file paths
    poly_file = os.path.join(base_dir, 'CapstoneDataset2024/Capstone_2024/Reference/Deprived_Areas/Lagos_Slum_reference.gpkg')
    raster_file = os.path.join(base_dir, 'CapstoneDataset2024/Capstone_2024/Dataset/Lagos/lagos_covariate_feature_53/lag_covariate_compilation_53bands.tif')
    output_file = os.path.join(base_dir, 'covariate/lagos_centroid.csv')

    # Create an instance of the Extractor class
    extractor = extract_by_point.Extractor(poly_file, raster_file, output_file)

    # Call the extract_data() method
    extractor.extract_data()

    #Step-2
    gpkg_path = os.path.join(base_dir, 'CapstoneDataset2024/Capstone_2024/Reference/Deprived_Areas/100mGrid_Lagos.gpkg')
    tif_directory = os.path.join(base_dir, 'context/lagos_contextual_10m')
    output_dir = os.path.join(base_dir, 'context/contextual_features_extraction_1')
    processor = extract_context_by_point.TIFFProcessor(gpkg_path, tif_directory, output_dir)
    processor.process_all_tifs()

    #Step-3
    input_dir = os.path.join(base_dir, 'context/contextual_features_extraction_1')
    output_file = os.path.join(base_dir, 'context/merged_all_feature_1.csv')
    concatenator = merging_contextual_feature.CSVConcatenator(input_dir, output_file)
    concatenator.concat_csv_files()

    #Step-4
    gpkg_file = os.path.join(base_dir, 'CapstoneDataset2024/Capstone_2024/Reference/Deprived_Areas/100mGrid_Lagos.gpkg')
    tif_file = os.path.join(base_dir, 'raw_image/lag_bgrn.tif')
    output_csv = os.path.join(base_dir, 'raw_image/lagos_bgrn.csv')
    extractor = coordinate_pixel_extraction.ExtractRasterValues(gpkg_file, tif_file, output_csv)
    extractor.extract_values()

    #Step-5
    covariate_file = os.path.join(base_dir, 'covariate/lagos_centroid.csv')
    merged_contextual_feature_file = os.path.join(base_dir, 'context/merged_all_feature_1.csv')
    bgrn_file = os.path.join(base_dir, 'raw_image/lagos_bgrn.csv')
    output_file = os.path.join(base_dir, 'combined_data/final_output_lagos.csv')
    merger = combined_data_1.CSVMerger(covariate_file, merged_contextual_feature_file, bgrn_file, output_file)
    merger.merge_csvs_on_geometry()

