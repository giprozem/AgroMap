from osgeo import gdal


def cutting_tiff(outputpath, inputpath, polygon):

    cutted_image = gdal.Warp(destNameOrDestDS=outputpath,
                             srcDSOrSrcDSTab=inputpath,
                             cutlineDSName=polygon,
                             cropToCutline=True,
                             copyMetadata=True,
                             dstNodata=0)
    cutted_image = None
