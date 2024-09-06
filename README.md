# Capstone-Group1 -- Geospatial Data Pipeline Processing and Modelling for Lagos, including Resampling Processing

## Overview
The dataset used for analyzing slums in Lagos contains 305,381 rows and 204 columns, which include:

1. Pixel Values: 4 features from the Sentinel-2 satellite image, representing different spectral bands (Red, Blue, Green, and Near-Infrared).
2. Covariate Features: 53 variables that include data which help in understanding the factors influencing the slum areas.
3. Contextual Features: 144 features representing a variety of attributes, such as building counts, density, climate risk factors, housing quality, extreme temperatures, population density, and even the differentiation between urban and rural areas, along with nocturnal lighting.
4. Geospatial Coordinates: Data includes longitude and latitude, facilitating precise location mapping.
5. Slum Labeling Scheme: The slum labels are categorized into 0, 1, 2, and 3. In the modeling:
   - 0 indicates non-deprived areas.
   - 1 and 2 are combined to denote deprived areas, capturing the broader spectrum of slum-like conditions.
   - 3 is excluded from the analysis due to uncertainty about its classification, ensuring data integrity and reliability.


Modeling Approach:
1. Tool Used: PyCaret, a machine learning library in Python, simplifies the model development process.
2. Data Split: The standard 70% training and 30% testing split provides a robust dataset for training while reserving a substantial portion for validating the model's performance.

## Installation steps
```
pip install -r src/requirements.txt
```
Build GDAL library from source
```
cd ~
cd ../../tmp/
wget https://download.osgeo.org/gdal/2.2.4/gdal-2.2.4.tar.gz
tar xzf gdal-2.2.4.tar.gz
cd gdal-2.2.4
./configure
make
sudo make install

```
Install GeoWombat
```
pip install git+https://github.com/jgrss/geowombat
sudo apt update -y && apt upgrade -y && \
apt install -y software-properties-common && \
add-apt-repository ppa:ubuntugis/ppa && \
apt update -y && apt install -y \
gdal-bin \
geotiff-bin \
git \
libgdal-dev \
libgl1 \
libspatialindex-dev \
wget \
python3 \
python3-pip \
pip \
g++
```

## Processes and Scripts

### 1. Initial Covariate Data and Slum Label Extraction
- **Objective**: Extract slum labels, geometric points, and 53 covariate band values.
- **Script**: `extract_by_point.py`
- **Inputs**:
  - `Lagos_Slum_reference.gpkg`: Contain slum labels for Lagos. 
  - `lag_covariate_compilation_53bands.tif`: Contains 53 covariate band values.
- **Output**:
  - `lagos_centroid.csv`: Contains slum labels, geometric points, and 53 covariate band values.

### 2.1 Resampling Contextual TIFF files with 10-meter resolution
- **Objective**: Resample 144 individual TIFF files with 10m resolution.
- **Script**: `context_resampled_100m.py`
- **Inputs**:
  - `Lagos_Contextual_10m`: Contains 144 individual contextual feature TIFF files.
- **Output**:
  - Directory `resampled_contextual_data_100m` with 144 individual TIFF files with 100m resolution.

### 2.2 Extracting Contextual Features
- **Objective**: Retrieve geometric points and extract contextual features from 144 individual TIFF files with 100m resolution.
- **Script**: `extract_context_by_point.py`
- **Inputs**:
  - `100mGrid_Lagos.gpkg`. 
  - `resampled_contextual_data_100m`: Contains 144 individual contextual feature TIFF files with 100m resolution.
- **Output**:
  - Directory `contextual_features_extraction` with 144 CSV files, each holding contextual feature values for points.

### 2.3 Merging Contextual Features
- **Objective**: Combine the 144 individual CSV files into a single file.
- **Script**: `merging_contextual_feature.py`
- **Inputs**: 
  - 144 individual CSV files from the previous step.
- **Output**:
  - `merged_contextual_features.csv`: Consolidates all contextual data and geometric points.

### 3.1 Resampling a RBGN TIFF file
- **Objective**: Resample a RBGN TIFF file with 10m resolution.
- **Script**: `rbgn_resample.py`
- **Inputs**: 
  - `lag_bgrn.tif` TIFF image with 10m resolution.
- **Output**:
  - `lag_resampled_bgrn.tif` TIFF image with 100 resolution.

### 3.2 RBGN Data Extraction
- **Objective**: Retrieve geometric points and corresponding RBGN (Red, Blue, Green, Near-infrared) values.
- **Script**: `extract_by_points_lag_bgrn.py`
- **Inputs**:
  - `100mGrid_Lagos.gpkg`. 
  - `lag_resampled_bgrn.tif` TIFF image.
- **Output**:
  - `lagos_bgrn.csv`: Contains geometric points and RBGN values.

### 4. Data Integration
- **Objective**: Merge slum labels, contextual features, covariate band values, and RBGN values based on geometric points.
- **Script**: `combined_data.py`
- **Inputs**:
  - `lagos_centroid.csv`
  - `merged_contextual_features.csv`
  - `lagos_bgrn.csv`
- **Output**:
  - `final_output_lagos.csv`: A comprehensive CSV file integrating all extracted data.
 
### 5. Modelling for Machine Learning Using PyCaret
- **Objective**: Merge slum labels, contextual features, covariate band values, and RBGN values based on geometric points.
- **Script**: `modelling.py` & `modelling_balanced.py`
- **Inputs**:
  - `final_output_lagos.csv`
- **Output**:
  - `modelling_logs_imbalanced.text`: Modelling results for laogs with imbalanaced slum labels.
  - `modelling_logs_balanced.text`: Comprehensive modelling results for laogs with balanaced slum labels.


### 6. Data Pipeline Tree Overview
<img width="489" alt="Screen Shot 2024-04-22 at 5 42 25 PM" src="https://github.com/akhil97/Capstone-Group1/assets/97569608/2d55a5cb-228e-448a-86d0-8f3445af3dcd">
