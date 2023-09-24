from io import BytesIO

import matplotlib.pyplot as plt
import numpy
import numpy as np
import rasterio
from django.core.files.base import ContentFile


def get_region_of_interest(ndmi, multiplier=1 / 2):
    """
    This function calculates the mean value of the Normalized Difference Moisture Index (NDMI) for the center of an image.
    """
    # undo the background adjustment
    region = np.where(ndmi == -255, 0, ndmi)

    # mean of center rows
    center_row1 = np.mean(region[int(multiplier * len(region))])
    center_row2 = np.mean(region[int(multiplier * len(region)) + 1])

    # mean of both rows
    mean = (center_row1 + center_row2) / 2
    return mean


def get_ndmi(swir_file, nir_file):
    """
    This function calculates the NDMI for given Short-Wave Infrared (SWIR) and Near Infrared (NIR) images.
    """
    with rasterio.open(swir_file) as band_swir:
        swir = band_swir.read(1).astype('float64')
    with rasterio.open(nir_file) as band_nir:
        nir = band_nir.read(1).astype('float64')

    np.seterr(divide='ignore', invalid='ignore')
    # ndwi calculation, empty cells or nodata cells are reported as 0
    ndmi = np.where((nir == 0.) | (swir == 0.), -255, np.where((nir + swir) == 0., 0, (nir - swir) / (nir + swir)))

    return ndmi


def ndmi_calculator(B08, B11, saving_file_name):
    """
    This function visualizes and calculates NDMI for given SWIR and NIR bands, and returns an image.
    """
    with rasterio.open(f'{B11}') as src:
        band_swir = src.read(1)

    with rasterio.open(f'{B08}') as f:
        band_nir = f.read(1)

    # Allow division by zero
    numpy.seterr(divide='ignore', invalid='ignore')

    # # Calculate NDMI
    ndmi = (band_nir.astype(float) - band_swir.astype(float)) / (band_nir + band_swir)

    min_value = numpy.nanmin(ndmi)
    max_value = numpy.nanmax(ndmi)
    mid = 0.1

    fig = plt.figure(figsize=(75, 25))
    ax = fig.add_subplot(111)

    cmap = 'Blues_r'
    cax = ax.imshow(ndmi, cmap=cmap, clim=(min_value, max_value), vmin=min_value, vmax=max_value)

    ax.axis('off')

    f = BytesIO()

    plt.savefig(f, format='png', transparent=True, bbox_inches='tight')
    content_file = ContentFile(f.getvalue())
    plt.close()
    return content_file


def average_ndmi(swir_file, nir_file):
    """
    This function calculates the average NDMI for given SWIR and NIR images.
    """
    return get_region_of_interest(get_ndmi(swir_file=swir_file, nir_file=nir_file))
