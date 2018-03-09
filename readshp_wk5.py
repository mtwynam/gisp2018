"""
Read shapefile and find out what's in it.

Specifically...
1. Format
2. CRS
3. Number of features
4. Geometry type
5. Bounding box coordinates
6. Schema (names/types for each attribute)

Tasks:
1. get/open shapefile
2. Get basic metadata
3. Get schema
4. iterate through features and display attribute data
"""

from osgeo import ogr
import fiona
from fiona.crs import from_epsg, from_string
import pyproj
import pycrs

SHAPEFILE = "../.cache/geoname_pop5000_geocoded.shp"
geojson = {"type": "FeatureCollection", "features": [], "crs": {"type": "EPSG", "properties": {"code": None}}, "bbox": []}

def main():
    try:
        print("\nGetting information for '{}'".format(SHAPEFILE))
        with fiona.open(SHAPEFILE, "r") as in_shape:
            this_proj = pyproj.Proj(in_shape.meta["crs"])
            newproj = pycrs.parser.from_unknown_wkt(in_shape.meta["crs_wkt"])
            fiproj = from_string(in_shape.meta["crs_wkt"])
            pass
    except Exception as e:
        print("{}".format(e))


if __name__ == "__main__":
    main()