# %%
import geopandas as gpd
import geowombat as gw

# %%
lagos_poly = gpd.read_file("100mGrid_Lagos.gpkg")
lagos_poly["geometry"] = lagos_poly.centroid

# %%

with gw.open(
    "lag_covariate_compilation_53bands.tif",
    # band_names=[""]
) as src:

    df = gw.extract(
        src,
        lagos_poly,
        nodata=-9999,
    )

    df.to_csv("lagos_centroid.csv", index=False)

# %%
