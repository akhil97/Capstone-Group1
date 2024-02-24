
# Import libraries
from glob import glob
import fiona
from subprocess import Popen
import geopandas as gpd
import rasterio
from rasterio import features
from rasterio.enums import Resampling
import numpy as np
import os
import matplotlib.pyplot as plt
#from osgeo import gdal, ogr
#gdal.SetConfigOption('SHAPE_RESTORE_SHX', 'YES')


# zip polygon and raster in to a list of tuple
RasterTiles = sorted(glob("../Data/nairobi.tif"))
polygons = sorted(glob('../../../Data/accra-20240218T210657Z-007/accra/temp/ClipPolygon/*.shp'))
shp_rast = zip(polygons, RasterTiles)
lst = list(shp_rast)

def resample_tiff(input_tiff, upscale_factor):
    """
       Load raster data and resample it.
       Args:
           input_tiff (str): Path to the raster file.
           resampling_factor (int): Factor by which to resample the raster.
       Returns:
           resampled_dataset: Resampled raster dataset.
    """
    with rasterio.open(input_tiff) as dataset:
        # resample data to target shape
        data = dataset.read(
            out_shape=(
                dataset.count,
                int(dataset.height * upscale_factor),
                int(dataset.width * upscale_factor)
            ),
            resampling=Resampling.bilinear
        )

        # scale image transform
        transform = dataset.transform * dataset.transform.scale(
            (dataset.width / data.shape[-1]),
            (dataset.height / data.shape[-2])
        )
        return transform


def rasterize_me(input_list, outfile):
    # read shapfile
    for i in input_list:
        resampled_tiff = resample_tiff(i[1], 10)
        df = gpd.read_file(i[0])
        df['id'] = np.random.randn(1)
        # add output file name
        head, tail = os.path.split(i[0])
        name=tail[:-4]
    # read raster
        with rasterio.open(resampled_tiff, mode="r") as src:
            out_arr = src.read(1)
            out_profile = src.profile.copy()
            out_profile.update(count=1,
                            nodata=-9999,
                            dtype='float32',
                            width=src.width,
                            height=src.height,
                            crs=src.crs)
            dst_height = src.height
            dst_width = src.width
            shapes = ((geom,value) for geom, value in zip(df.geometry, df.id))
            # print(shapes)
            burned = features.rasterize(shapes=shapes, out_shape=(dst_height, dst_width),fill=0, transform=src.transform)
            plt.imshow(burned)

        # open in 'write' mode, unpack profile info to dst
        with rasterio.open(f'{outfile}{name}.tif',
                        'w', **out_profile) as dst:
            dst.write_band(1, burned)

#polygons = sorted(glob('.shp'))
#RasterTiles = sorted(glob("D:/GWU/ML4DAM/data/accra/final/spfea/*.tif"))
outfile = '../../../Data/accra/mask/'

rasterize_me(input_list = lst, outfile=outfile)
# %%

