import geopandas as gpd
import geowombat as gw

# Read a GeoPackage containing polygons
lagos_poly = gpd.read_file("100mGrid_Lagos.gpkg")
# Replace the geometry of each polygon with its centroid
lagos_poly["geometry"] = lagos_poly.centroid

# Open a raster file that contains a resampled tif file with lagos_bgrn
with gw.open(
    "lag_bgrn.tif",
) as src:
    # Extract raster values using the centroids of the polygons defined in 'lagos_poly'
    df = gw.extract(
        src,
        lagos_poly,
        nodata=-9999,
    )

    # Rename columns in the extracted DataFrame
    df.rename(columns={1: 'bgrn_1', 2: 'bgrn_2', 3: 'bgrn_3', 4: 'bgrn_4'}, inplace=True)

    # Save the extracted data to a CSV file
    df.to_csv("lagos_bgrn.csv", index=False)

