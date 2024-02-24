# Resampling of Raster Images from 10m to 100m Resolution
## contex_resampled_100m.py
The provided Python script resamples raster images, specifically TIFF files, from a 10m resolution to a 100m resolution. It achieves this by setting a resampling factor of 0.1, effectively reducing the pixel density to one-tenth of the original. The resampling is done using bilinear interpolation, which helps maintain data continuity in the newly scaled images. The script scans a specified directory for TIFF files, processes each file by resampling it, and saves the resampled output in a new file.

# Extracting Contextual Features from the resampled data
## contextual_feature_extraction.py
The Python script extracts contextual features from resampled TIFF raster files and converts them to CSV format. It retrieves geographical coordinates from each raster, adjusts these coordinates for a westward and northward shift of approximately 1000 meters, and samples the raster values at these new locations. The extracted data, comprising longitude, latitude, and raster values, is then saved as CSV files, with each file corresponding to a raster image. 
