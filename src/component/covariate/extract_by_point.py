import geopandas as gpd
import geowombat as gw

class Extractor:
    def __init__(self, poly_file, raster_file, output_file):
        self.poly_file = poly_file
        self.raster_file = raster_file
        self.output_file = output_file

    def extract_data(self):
        # Read a GeoPackage containing polygons and slum labels
        lagos_poly = gpd.read_file(self.poly_file)

        # Replace the geometry of each polygon with its centroid
        lagos_poly["geometry"] = lagos_poly.centroid

        # Open a raster file that contains covariate data for Lagos with 53 bands
        with gw.open(self.raster_file) as src:
            # Extract raster values using the centroids of the polygons defined in 'lagos_poly'
            df = gw.extract(
                src,
                lagos_poly,
                nodata=-9999,
            )

            # Save the extracted data to a CSV file which has included slum labels
            df.to_csv(self.output_file, index=False)