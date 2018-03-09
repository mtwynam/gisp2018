import geopy_corrected as gc
import json

my_location = "255000.0, 333000"
epsg_code = 29902
result = gc.geocode_location(my_location, epsg_code)
result["body"] = json.loads(result["body"])

print("Geocoded {} with CRS {}. Result is {}".format(my_location, epsg_code, result))