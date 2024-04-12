# Capstone-Group1 -- Geospatial Data Pipeline Processing for Lagos

## Overview
This project involves extracting slum labels, geometric points, RBGN values, and various covariate and contextual feature values from multiple geospatial data sources. The output is a comprehensive CSV file that integrates all extracted data aligned by geometric points, suitable for further analysis or modeling.

## Processes and Scripts

### 1. Initial Covariate Data and Slum Label Extraction
- **Objective**: Extract slum labels, geometric points, and 53 covariate band values.
- **Script**: `extract_by_point.py`
- **Inputs**:
  - A reference GPKG file for Lagos.
  - A covariate TIFF file that includes 53 band values.
- **Output**:
  - `lagos_centroid.csv`: Contains slum labels, geometric points, and 53 covariate band values.

### 2. Extracting Contextual Features
- **Objective**: Retrieve geometric points and extract contextual features from 144 individual TIFF files.
- **Script**: `extract_context_by_point.py`
- **Inputs**:
  - A '100mGrid_Lagos.gpkg' file. 
  - 144 individual contextual feature TIFF files.
- **Output**:
  - Directory `contextual_features_extraction` with 144 CSV files, each holding contextual feature values for points.

### 3. Merging Contextual Features
- **Objective**: Combine the 144 individual CSV files into a single file.
- **Script**: `merging_contextual_feature.py`
- **Inputs**: 
  - 144 individual CSV files from the previous step.
- **Output**:
  - `merged_contextual_features.csv`: Consolidates all contextual data and geometric points.

### 4. RBGN Data Extraction
- **Objective**: Retrieve geometric points and corresponding RBGN (Red, Blue, Green, Near-infrared) values.
- **Script**: `extract_by_points_lag_bgrn.py`
- **Inputs**:
  - A `100mGrid_Lagos.gpkg` file. 
  - `lag_bgrn.tif` TIFF image.
- **Output**:
  - `lagos_bgrn.csv`: Contains geometric points and RBGN values.

### 5. Data Integration
- **Objective**: Merge slum labels, contextual features, covariate band values, and RBGN values based on geometric points.
- **Script**: `combined_data.py`
- **Inputs**:
  - `lagos_centroid.csv`
  - `merged_contextual_features.csv`
  - `lagos_bgrn.csv`
- **Output**:
  - `final_output_lagos.csv`: A comprehensive CSV file integrating all extracted data.
