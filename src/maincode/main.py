import os
import sys

project_path = '/home/ubuntu/Cap2024'
sys.path.append(project_path)

from src.component.covariate import extract_by_point

from src.component.contextual import context_resampled_100m
from src.component.contextual import extract_context_by_point
from src.component.contextual import merging_contextual_feature

from src.component.rawimageproc import rbgn_resample
from src.component.rawimageproc import coordinate_pixel_extraction

from src.component.combinedata import combined_data


if __name__ == '__main__':
    # Define base directory
    base_dir = project_path

    # Step-1
    # Define file paths
    poly_file = os.path.join(base_dir, '../../../Data/Lagos_Slum_reference.gpkg')
    raster_file = os.path.join(base_dir, '../../../Data/lag_covariate_compilation_53bands.tif')
    output_file = os.path.join(base_dir, 'covariate/lagos_centroid.csv')

    # Create an instance of the Extractor class
    extractor = extract_by_point.Extractor(poly_file, raster_file, output_file)

    # Call the extract_data() method
    extractor.extract_data()

    #Step-2.1
    input_dir = os.path.join(base_dir, '../../../Data/lagos_contextual_10m')
    output_dir = os.path.join(base_dir, 'context/resampled_contextual_data_100m')
    resampler = context_resampled_100m.TIFFResampler(input_dir, output_dir)
    resampler.process_all_files()

    # Step-2.2
    gpkg_path = os.path.join(base_dir, '../../../Data/100mGrid_Lagos.gpkg')
    resampled_tif_dir = os.path.join(base_dir, 'context/resampled_contextual_data_100m')
    output_dir = os.path.join(base_dir, 'context/contextual_features_extraction')
    processor = extract_context_by_point.TIFFProcessor(gpkg_path, resampled_tif_dir, output_dir)
    processor.process_all_tifs()

    #Step-2.3
    input_dir = os.path.join(base_dir, 'context/contextual_features_extraction')
    output_file = os.path.join(base_dir, 'context/merged_all_feature.csv')
    concatenator = merging_contextual_feature.CSVConcatenator(input_dir, output_file)
    concatenator.concat_csv_files()

    #Step-3.1
    file_path = os.path.join(base_dir, '../../../Data/lag_bgrn.tif')
    output_path = os.path.join(base_dir, 'raw_image/lag_resampled_bgrn.tif')
    resampler = rbgn_resample.RasterResampler(file_path, output_path)
    resampler.resample_bgrn_raster()

    # Step-3.2
    gpkg_file = os.path.join(base_dir, '../../../Data/100mGrid_Lagos.gpkg')
    tif_file = os.path.join(base_dir, 'raw_image/lag_resampled_bgrn.tif')
    output_csv = os.path.join(base_dir, 'raw_image/lagos_resampled_bgrn.csv')
    extractor = coordinate_pixel_extraction.ExtractRasterValues(gpkg_file, tif_file, output_csv)
    extractor.extract_values()

    #Step-4
    covariate_file = os.path.join(base_dir, 'covariate/lagos_centroid.csv')
    merged_contextual_feature_file = os.path.join(base_dir, 'context/merged_all_feature.csv')
    bgrn_file = os.path.join(base_dir, 'raw_image/lagos_resampled_bgrn.csv')
    output_file = os.path.join(base_dir, 'combined_data/final_output_lagos_100m.csv')
    merger = combined_data_1.CSVMerger(covariate_file, merged_contextual_feature_file, bgrn_file, output_file)
    merger.merge_csvs_on_geometry()
