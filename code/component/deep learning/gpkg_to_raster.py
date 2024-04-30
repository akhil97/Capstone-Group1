import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_bounds

gpkg_path = r'/home/ubuntu/Cap2024/CapstoneDataset2024/Capstone_2024/Reference/Deprived_Areas/Lagos_Slum_reference.gpkg'
output_raster_path = r'/home/ubuntu/Cap2024/DL/lagos_slum_10m.tif'

# Load the GeoPackage file
df = gpd.read_file(gpkg_path)

# fill 0 to the 'Slum' column
df['Slum'] = df['Slum'].fillna(0).astype(int)

# Set the resolution to 10 meters per pixel
pixel_size = 10

# Calculate the number of pixels based on the 10-meter resolution
width = int((df['geometry'].total_bounds[2] - df['geometry'].total_bounds[0]) / pixel_size)
height = int((df['geometry'].total_bounds[3] - df['geometry'].total_bounds[1]) / pixel_size)

# Define the transformation for 10-meter resolution
transform = from_bounds(*df['geometry'].total_bounds, width, height)

# Rasterize the data
rasterized_data = rasterize(
    [(geom, label) for geom, label in zip(df['geometry'], df['Slum'])],
    out_shape=(height, width),
    transform=transform,
    fill=0,
    all_touched=True,
    dtype=rasterio.uint8
)

# Save the rasterized data
with rasterio.open(
        output_raster_path, 'w',
        driver='GTiff',
        dtype=rasterio.uint8,
        count=1,
        width=width,
        height=height,
        crs=df.crs,
        transform=transform
) as dst:
    dst.write(rasterized_data, indexes=1)
