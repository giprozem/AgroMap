from osgeo import gdal


def cutting_tiff(outputpath, inputpath, polygon, x_res=None, y_res=None):
    options = {
        "destNameOrDestDS": outputpath,
        "srcDSOrSrcDSTab": inputpath,
        "cutlineDSName": polygon,
        "cropToCutline": True,
        "copyMetadata": True,
        "dstNodata": 0
    }

    if x_res and y_res:
        options["xRes"] = x_res
        options["yRes"] = y_res

    cutted_image = gdal.Warp(**options)
    cutted_image = None
