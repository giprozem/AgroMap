from io import BytesIO

import matplotlib.pyplot as plt
import numpy
import numpy as np
import rasterio
from django.core.files.base import ContentFile


def get_region_of_interest(ndwi, multiplier=1 / 2):
    """
    This function calculates the mean value of the Normalized Difference Water Index (NDWI) for the center of an image.
    """
    # undo the background adjustment
    region = np.where(ndwi == -255, 0, ndwi)

    # mean of center rows
    center_row1 = np.mean(region[int(multiplier * len(region))])
    center_row2 = np.mean(region[int(multiplier * len(region)) + 1])

    # mean of both rows
    mean = (center_row1 + center_row2) / 2
    return round(mean, 3)


def get_ndwi(green_file, nir_file):
    """
    This function calculates the NDWI using Green and Near Infrared (NIR) bands.
    """
    with rasterio.open(green_file) as band_green:
        green = band_green.read(1).astype('float64')

    with rasterio.open(nir_file) as band_nir:
        nir = band_nir.read(1).astype('float64')

    np.seterr(divide='ignore', invalid='ignore')
    # ndwi calculation, empty cells or nodata cells are reported as 0
    ndwi = np.where((green == 0.) | (nir == 0.), -255, np.where((green + nir) == 0., 0, (green - nir) / (green + nir)))

    return ndwi


def ndwi_calculator(B03, B08, saving_file_name):
    """
    This function visualizes and calculates NDWI for the provided Green and NIR bands, and returns an image.
    """
    # Open the Green band using rasterio and read the data
    with rasterio.open(B03) as src:
        band_green = src.read(1)

    # Open the NIR band using rasterio and read the data
    with rasterio.open(B08) as f:
        band_nir = f.read(1)

    # Allow division by zero
    numpy.seterr(divide='ignore', invalid='ignore')

    # Calculate NDWI
    ndwi = (band_green.astype(float) - band_nir.astype(float)) / (band_green + band_nir)

    # Find the minimum and maximum values of NDWI
    min_value = numpy.nanmin(ndwi)
    max_value = numpy.nanmax(ndwi)

    # Create a figure and axis to visualize the NDWI
    fig, ax = plt.subplots(figsize=(75, 25))

    # Define a colormap for visualization
    cmap = 'winter'

    # Display the NDWI data
    ax.imshow(ndwi, cmap=cmap, clim=(min_value, max_value), vmin=min_value, vmax=max_value)

    # Turn off the axis
    ax.axis('off')

    # Adjust the figure to remove borders and whitespace
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0, hspace=0, wspace=0)
    ax.margins(0, 0)
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())

    # Save the figure to a BytesIO object
    f = BytesIO()
    fig.savefig(f, format="png", bbox_inches='tight', transparent=True, pad_inches=0)

    # Close the figure to free memory
    plt.close(fig)

    # Convert the BytesIO object to a Django ContentFile
    content_file = ContentFile(f.getvalue())

    return content_file


def average_ndwi(green_file, nir_file):
    """
    This function calculates the average NDWI for given Green and NIR images.
    """
    return get_region_of_interest(get_ndwi(green_file=green_file, nir_file=nir_file))
