# Resampling of Raster Images from 10m to 100m Resolution
## contex_resampled_100m.py
The Python script resamples raster images, specifically a total of 144 TIFF files, from a 10m resolution to a 100m resolution. It achieves this by setting a resampling factor of 0.1, effectively reducing the pixel density to one-tenth of the original. The resampling is done using bilinear interpolation, which helps maintain data continuity in the newly scaled images. The script scans a specified directory for TIFF files, processes each file by resampling it, and saves the resampled output in a new file.

# Extracting Contextual Features from the resampled data
## contextual_feature_extraction.py
The Python script extracts contextual features from 144 resampled TIFF raster files and converts them to CSV format. It retrieves geographical coordinates from each raster, adjusts these coordinates for a westward and northward shift of approximately 1000 meters, and samples the raster values at these new locations. The extracted data, comprising longitude, latitude, and raster values, is then saved as CSV files, with each file corresponding to a raster image. 

# Merging Contextual Features
## merging_contextual_feature.py
The Python script streamlines the merging of multiple CSV files into one, focusing on combining raster value data with geographical coordinates. It first establishes a base dataframe using longitude and latitude from the first CSV file in the specified directory. The script then iterates through each CSV file, extracting and storing the 'Raster Value' column in a dictionary. These values are concatenated and merged with the base dataframe to create a comprehensive dataset that aligns raster values with corresponding coordinates. Finally, the merged data is saved into a new CSV file.
