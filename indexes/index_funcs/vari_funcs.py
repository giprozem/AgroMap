from io import BytesIO

import matplotlib.pyplot as plt
import numpy
import numpy as np
import rasterio
from django.core.files.base import ContentFile


def get_region_of_interest(vari, multiplier=1 / 2):
    # undo the background adjustment
    region = np.where(vari == -255, 0, vari)

    # mean of center rows
    center_row1 = np.mean(region[int(multiplier * len(region))])
    center_row2 = np.mean(region[int(multiplier * len(region)) + 1])

    # mean of both rows
    mean = (center_row1 + center_row2) / 2
    return round(mean, 3)


def get_vari(red_file, green_file, blue_file):
    with rasterio.open(red_file) as band_red:
        red = band_red.read(1).astype('float64')

    with rasterio.open(green_file) as band_green:
        green = band_green.read(1).astype('float64')

    with rasterio.open(blue_file) as band_blue:
        blue = band_blue.read(1).astype('float64')

    np.seterr(divide='ignore', invalid='ignore')
    # vari calculation, empty cells or nodata cells are reported as 0
    vari = np.where((green == 0.) | (red == 0.) | (blue == 0.), -255,
                    np.where((green - red - blue) == 0., 0, (green - red) / (green + red - blue)))

    return vari


def vari_calculator(B02, B03, B04, saving_file_name):
    with rasterio.open(f'{B02}') as blue:
        band_blue = blue.read(1)

    with rasterio.open(f'{B03}') as green:
        band_green = green.read(1)

    with rasterio.open(f'{B04}') as red:
        band_red = red.read(1)

    # Allow division by zero
    numpy.seterr(divide='ignore', invalid='ignore')

    # # Calculate vari
    vari = ((band_green.astype(float) - band_red.astype(float)) / (band_green + band_red - band_blue))

    min_value = numpy.nanmin(vari)
    max_value = numpy.nanmax(vari)
    mid = 0.1

    fig = plt.figure(figsize=(75, 25))
    ax = fig.add_subplot(111)

    cmap = 'RdYlGn'
    cax = ax.imshow(vari, cmap=cmap, clim=(min_value, max_value), vmin=min_value, vmax=max_value)

    ax.axis('off')

    f = BytesIO()

    f = BytesIO()

    plt.savefig(f, format='png', transparent=True, bbox_inches='tight')
    content_file = ContentFile(f.getvalue())
    plt.close()
    return content_file


def average_vari(red_file, green_file, blue_file):
    return get_region_of_interest(get_vari(red_file=red_file, green_file=green_file, blue_file=blue_file))
