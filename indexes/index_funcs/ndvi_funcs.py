from io import BytesIO

import numpy
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from django.core.files.base import ContentFile


def get_region_of_interest(ndvi, multiplier=1 / 2):
    """
    This function calculates the mean value of the Normalized Difference Vegetation Index (NDVI) for the center of an image.
    """
    # undo the background adjustment
    region = np.where(ndvi == -255, 0, ndvi)

    # mean of center rows
    center_row1 = np.mean(region[int(multiplier * len(region))])
    center_row2 = np.mean(region[int(multiplier * len(region)) + 1])

    # mean of both rows
    mean = (center_row1 + center_row2) / 2
    return round(mean, 3)


def get_ndvi(red_file, nir_file):
    """
    This function calculates the NDVI for given Red and Near Infrared (NIR) images.
    """
    with rasterio.open(red_file) as band_red:
        red = band_red.read(1).astype('float64')

    with rasterio.open(nir_file) as band_nir:
        nir = band_nir.read(1).astype('float64')

    np.seterr(divide='ignore', invalid='ignore')
    # ndvi calculation, empty cells or nodata cells are reported as 0
    ndvi = np.where((nir == 0.) | (red == 0.), -255, np.where((nir + red) == 0., 0, (nir - red) / (nir + red)))

    return ndvi


def ndvi_calculator(B04, B08, saving_file_name):
    """
    This function visualizes and calculates NDVI for the provided Red and NIR bands, and returns an image.
    """
    # Open the Red band using rasterio and read the data
    with rasterio.open(B04) as src:
        band_red = src.read(1)

    # Open the NIR band using rasterio and read the data
    with rasterio.open(B08) as f:
        band_nir = f.read(1)

    # Set numpy error handling
    numpy.seterr(divide='ignore', invalid='ignore')

    # Calculate NDVI
    ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)

    # Find the minimum and maximum values of NDVI
    min_value = numpy.nanmin(ndvi)
    max_value = numpy.nanmax(ndvi)

    # Create a figure and axis to visualize the NDVI
    fig, ax = plt.subplots(figsize=(75, 25))

    # Define a colormap for visualization
    cmap = plt.cm.YlGn

    # Display the NDVI data
    ax.imshow(ndvi, cmap=cmap, clim=(min_value, max_value), vmin=min_value, vmax=max_value)

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


def average_ndvi(red_file, nir_file):
    """
    This function calculates the average NDVI for given Red and NIR images.
    """
    return get_region_of_interest(get_ndvi(red_file=red_file, nir_file=nir_file))
