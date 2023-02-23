from io import BytesIO

import matplotlib.pyplot as plt
import numpy
import numpy as np
import rasterio
from django.core.files.base import ContentFile


def get_region_of_interest(ndwi, multiplier=1/2):

    # undo the background adjustment
    region = np.where(ndwi == -255, 0, ndwi)

    # mean of center rows
    center_row1 = np.mean(region[int(multiplier * len(region))])
    center_row2 = np.mean(region[int(multiplier * len(region)) + 1])

    # mean of both rows
    mean = (center_row1 + center_row2) / 2
    return round(mean, 3)


def get_ndwi(green_file, nir_file):
    with rasterio.open(green_file) as band_green:
        green = band_green.read(1).astype('float64')

    with rasterio.open(nir_file) as band_nir:
        nir = band_nir.read(1).astype('float64')

    np.seterr(divide='ignore', invalid='ignore')
    # ndwi calculation, empty cells or nodata cells are reported as 0
    ndwi = np.where((green == 0.) | (nir == 0.), -255, np.where((green + nir) == 0., 0, (green - nir) / (green + nir)))

    return ndwi


def ndwi_calculator(B03, B08, saving_file_name):

    with rasterio.open(f'{B03}') as src:
        band_green = src.read(1)

    with rasterio.open(f'{B08}') as f:
        band_nir = f.read(1)

    # Allow division by zero
    numpy.seterr(divide='ignore', invalid='ignore')

    # # Calculate ndwi
    ndwi = (band_green.astype(float) - band_nir.astype(float)) / (band_green + band_nir)

    min_value = numpy.nanmin(ndwi)
    max_value = numpy.nanmax(ndwi)
    mid = 0.1

    fig = plt.figure(figsize=(75, 25))
    ax = fig.add_subplot(111)

    cmap = 'winter'
    cax = ax.imshow(ndwi, cmap=cmap, clim=(min_value, max_value), vmin=min_value, vmax=max_value)

    ax.axis('off')

    f = BytesIO()

    plt.savefig(f, format='png', transparent=True, bbox_inches='tight')
    content_file = ContentFile(f.getvalue())
    plt.close()
    return content_file


def average_ndwi(green_file, nir_file):
    return get_region_of_interest(get_ndwi(green_file=green_file, nir_file=nir_file))
