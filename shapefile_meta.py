#!/usr/bin/env python3
"""
Take any shapefile and find out what's in it such as
1. Format - will be "ESRI Shapefile"
2. CRS
3. Geometry type
4. Schema
5. Number of features
6. Bounding Box
7. Attibute data for each feature
8. BBOX for each feature
9. Create GeoJSON file to match shapefile
10.Create CSV file containing attribute data.
"""

import fiona, json

INPUT_SHAPEFILE = "counties/ctygeom.shp"


def main():
    """
    This program takes as input any shapefile and prints what's in it including
    1. Format - will be "ESRI Shapefile"
    2. CRS
    3. Geometry type
    4. Schema
    5. Number of features
    6. Bounding Box
    7. Attibute data for each feature

    It also creates output files containing a GeoJSON representation of the shapefile and a CSV file containing its
    attributes. These are named as per the shapefile but with the extensions changed to .json and .csv respectively.

    :param input_shapefile:
    :return: Nothing
    """
    # Ceate outline geojson structure
    geojson = {"type": "FeatureCollection", "features": [], "crs": {"type": "EPSG", "properties": {"code": None}},
               "bbox": []}

    num_ticks = 60
    # input_shapefile = input("Enter the path (if necessary) and name fo the input shapefile: ")

    # print("{}".format("=" * num_ticks))
    # print("Getting information for '{}'".format(input_shapefile))
    # print("{}\n".format("-" * num_ticks))
    print("Getting information for '{}'".format(INPUT_SHAPEFILE))

    try:
        with fiona.open(INPUT_SHAPEFILE, "r") as fh:
            print("Driver:  \t{}".format(fh.driver))
            print("Encoding:\t{}".format(fh.encoding))
            print("Geometry:\t{}".format(fh.schema["geometry"]))
            print("CRS:     \t{}".format(fh.crs["init"].upper()))
            print("Bounds:  \t{}".format(fh.bounds))
            print("Features \t{}".format(len(fh)))

            print("Attribute Types")

            # Add crs and bbox properties to the geojson structure
            geojson["crs"]["properties"]["code"] = int(fh.crs["init"].split(":")[1])
            geojson["bbox"] = fh.bounds

            header_string = ""
            csv_header = ""
            for k, v in fh.schema["properties"].items():
                print("\t{:10}\t{}".format(k, v))
                header_string += "\t{:>30}".format(k)
                csv_header += "{}\t".format(k)
            print("\n" + header_string)

            with open(INPUT_SHAPEFILE.split(".")[0] + ".csv", "w") as fh_csv:
                fh_csv.write("{}\n".format(csv_header[:-1]))
                for feature in fh:
                    # add each feature to geojson structure, Fiona gives it to us in a suitable format so no further processing
                    # required
                    geojson["features"].append(feature)

                    data_string = ""
                    csv_data = ""
                    for k, v in feature["properties"].items():
                        data_string += "\t{:>30}".format(v)
                        csv_data += "{}\t".format(v)
                    print(data_string)
                    fh_csv.write("{}\n".format(csv_data[:-1]))

        # Create output geojson file and convert geojson python stucture to json
        with open(INPUT_SHAPEFILE.split(".")[0] + ".json", "w") as fh:
            fh.write(json.dumps(geojson))

    except Exception as e:
        print(e)
        quit()
    finally:
        print("{}".format("=" * num_ticks))


if __name__ == "__main__":
    main()
