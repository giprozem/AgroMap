from osgeo import gdal
import os
from indexes.models.satelliteimage import SciHubImageDate
import rasterio
import numpy as np
import matplotlib.pyplot as plt


def cut_image():
    satellite = SciHubImageDate.objects.last()

    in_path = '/usr/src/app/media/RGB/file.tif'

    ds = gdal.Open(in_path)
    band = ds.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize

    out_path = '/usr/src/app/media/images/tiff/'
    output_filename = f'tile_B0{n}'

    tile_size_x = 256
    tile_size_y = 256

    for i in range(0, xsize, tile_size_x):
        for j in range(0, ysize, tile_size_y):
            com_string = "gdal_translate -of GTIFF -srcwin " + str(i) + ", " + str(j) + ", " + \
                          str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + str(input_filename) + \
                          " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
            os.system(com_string)


def create_rgb():
    satellite = SciHubImageDate.objects.last()
    print(satellite)

    # path = '/usr/src/app/media/satellite_images/'
    # files = [
    #     path + satellite.B02,  # Blue
    #     path + satellite.B03,  # Green
    #     path + satellite.B04,  # Red
    # ]
    # src = rasterio.open(path[0])
    #
    # meta = src.meta
    # meta.update(count=len(files))
    # meta.update(driver="GTiff")
    # with rasterio.open("/usr/src/app/media/RGB/file.tif", "w", **meta) as dst:
    #     for id, layer in enumerate(files, start=1):
    #         with rasterio.open(layer) as src:
    #             dst.write(src.read(1), id)
    #
    # with rasterio.open('/usr/src/app/media/RGB/file.tif') as src:
    #     red = src.read(3)
    #     green = src.read(2)
    #     blue = src.read(1)
    #
    #     # Scale the bands to the 0-255 range
    #     red = np.interp(red, (red.min(), red.max()), (0, 255)).astype('uint8')
    #     green = np.interp(green, (green.min(), green.max()), (0, 255)).astype('uint8')
    #     blue = np.interp(blue, (blue.min(), blue.max()), (0, 255)).astype('uint8')
    #
    #     # Create an RGB image by stacking the bands
    #     rgb = np.dstack((red, green, blue))
    #
    #     # Get metadata from the source file and update the count and data type
    #     meta = src.meta.copy()
    #     meta.update(count=3, dtype='uint8')
    #
    #     # Write the RGB image to a new GeoTIFF file
    #     with rasterio.open('/usr/src/app/media/RGB/file.tif', 'w', **meta) as dst:
    #         dst.write(rgb.transpose(2, 0, 1))
