import geopandas as gpd
import geowombat as gw

# Read a GeoPackage containing polygons
lagos_poly = gpd.read_file("100mGrid_Lagos.gpkg")

# Replace the geometry of each polygon with its centroid
lagos_poly["geometry"] = lagos_poly.centroid

# Open a raster file that contains covariate data for Lagos with 53 bands
with gw.open(
    "lag_covariate_compilation_53bands.tif",
) as src:
    # Extract raster values using the centroids of the polygons defined in 'lagos_poly'
    df = gw.extract(
        src,
        lagos_poly,
        nodata=-9999,
    )
    
    # Save the extracted data to a CSV file
    df.to_csv("lagos_centroid.csv", index=False)
