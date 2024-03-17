import numpy as np
import geopandas as gpd
import rasterio
from shapely.geometry import Point

# This code runs after having training file which is a Geotiff file that contains
# the labeled areas on 100m2 level using the survey framework arranged by Idea Maps Network (https://ideamapsnetwork.org/lagos-aos/)

# This file will then loop through all the meta data in the file and extract the coordinates
# with its corresponding label in a csv


with rasterio.open('../../../Data/lag_bgrn_resampled_file.tif') as dataset:
    val = dataset.read(1) # band 1
    no_data=dataset.nodata
    geometry = [Point(dataset.xy(x,y)[0],dataset.xy(x,y)[1]) for x,y in np.ndindex(val.shape) if val[x,y] != no_data]
    v = [val[x,y] for x,y in np.ndindex(val.shape) if val[x,y] != no_data]
    ref_df = gpd.GeoDataFrame({'geometry':geometry,'label':v}, crs = 'ESRI:54009')

print(ref_df.head())