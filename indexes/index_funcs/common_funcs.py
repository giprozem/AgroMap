from osgeo import gdal


def cutting_tiff(outputpath, inputpath, polygon, x_res=None, y_res=None):
    """
    This function crops a GeoTIFF file based on a given polygon and saves the output to a specified path.
    """

    # Set the default options for gdal Warp.
    options = {
        "destNameOrDestDS": outputpath,  # Destination file path.
        "srcDSOrSrcDSTab": inputpath,  # Source file path.
        "cutlineDSName": polygon,  # Polygon for cropping.
        "cropToCutline": True,  # Crop to the given cutline.
        "copyMetadata": True,  # Copy the metadata from the source file.
        "dstNodata": 0  # Set no data value to 0.
    }

    # If the x and y resolutions are given, update the options.
    if x_res and y_res:
        options["xRes"] = x_res
        options["yRes"] = y_res

    # Use gdal Warp to crop the image.
    cutted_image = gdal.Warp(**options)
    cutted_image = None  # Close the dataset.
