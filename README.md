# Capstone-Group1 -- Geospatial Data Pipeline Processing and Modelling for Lagos and Nairobi including Resampling Processing

# Table of contents
- Dataset Overview
- Data pipeline diagram
- Scope of the project
- Modelling approach
- Installation steps
- Processes and scripts
- Data pipeline tree overview

# Dataset Overview
The dataset used for analyzing slums in Lagos contains 305,381 rows and 204 columns, which include:

1. Pixel Values: 4 features from the Sentinel-2 satellite image, representing different spectral bands (Red, Blue, Green, and Near-Infrared).
2. Covariate Features: 53 variables that include data that help understand the factors influencing the slum areas.
3. Contextual Features: 144 features representing a variety of attributes, such as building counts, density, climate risk factors, housing quality, extreme temperatures, population density, and even the differentiation between urban and rural areas, along with nocturnal lighting.
4. Geospatial Coordinates: Data includes longitude and latitude, facilitating precise location mapping.
5. Slum Labeling Scheme: The slum labels are categorized into 0, 1, 2, and 3. In the modelling:
   - 0 indicates non-deprived areas.
   - 1 and 2 are combined to denote deprived areas, capturing the broader spectrum of slum-like conditions.
   - 3 is excluded from the analysis due to uncertainty about its classification, ensuring data integrity and reliability.

# Data pipeline diagram
<img width="757" alt="Flowchart" src="https://github.com/user-attachments/assets/bb5f13d9-1018-417c-9b68-c912e49e261f" />

# Scope of the project
-Introduction <br>
The prevalence and growth of slums in low- and middle- income countries (LMICs) present a significant challenge especially during COVID-19 pandemic and economic crisis. <br>
Accurate mapping of deprived areas is important for monitoring Sustainable Development Goals (SDGs).  <br>
-The IDEAMAPS Project <br>
Aims to improve the consistency and accuracy of mapping deprived areas across cities, mainly focusing on African cities, specifically Lagos, Nigeria and Nairobi, Kenya.  <br>
-Data sources and metrics  <br>
Open geospatial data sources: Google Maps Engine & OpenStreetMap  <br>
Relevant datasets: sentinel-2 imagery, covariate features, and contextual features  <br>
-Model performance: F1 scores with balanced precision and recall values  <br>
The best-performing model will be determined by its ability to generalize and identify deprived areas across different urban settings  <br>

# Modelling approach:
1. Tool Used: PyCaret, a machine learning library in Python, simplifies the model development process.
2. Data Split: The standard 70% training and 30% testing split provides a robust dataset for training while reserving a substantial portion for validating the model's performance.

## Installation steps
```
pip install -r src/requirements.txt
```
Install GeoWombat
```
pip install git+https://github.com/jgrss/geowombat
sudo apt update -y && sudo apt upgrade -y && \
sudo apt install -y software-properties-common && \
sudo add-apt-repository ppa:ubuntugis/ppa && \
sudo apt update -y && sudo apt install -y \
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
  - `modelling_logs_imbalanced.text`: Modelling results for Lagos with imbalanced slum labels.
  - `modelling_logs_balanced.text`: Comprehensive modelling results for Lagos with balanced slum labels.



### 6. Data Pipeline Tree Overview
<img width="489" alt="Screen Shot 2024-04-22 at 5 42 25 PM" src="https://github.com/akhil97/Capstone-Group1/assets/97569608/2d55a5cb-228e-448a-86d0-8f3445af3dcd">

### 7. Mapping slum labels on QGIS for Lagos
<img width="632" height="393" alt="image" src="https://github.com/user-attachments/assets/3eb34262-291a-4142-a4ba-73824cba837a" />


