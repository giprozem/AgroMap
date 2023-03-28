from osgeo import gdal
import os
from indexes.models.satelliteimage import SciHubImageDate


def cut_image(satellite_image):
    satellite = SciHubImageDate.objects.get(id=satellite_image.pk)

    input_filename = satellite.B02

    out_path = 'images/tiff'
    output_filename = 'tile_B02'

    tile_size_x = 256
    tile_size_y = 256

    ds = gdal.Open(input_filename)
    band = ds.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize

    for i in range(0, xsize, tile_size_x):
        for j in range(0, ysize, tile_size_y):
            com_string = "gdal_translate -of GTIFF -srcwin " + str(i) + ", " + str(j) + ", " + \
                         str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + str(input_filename) + \
                         " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
            os.system(com_string)
