from io import BytesIO

import matplotlib.pyplot as plt
import numpy
import numpy as np
import rasterio
from django.core.files.base import ContentFile


def get_region_of_interest(savi, multiplier=1 / 2):
    """
    This function calculates the mean value of the Soil Adjusted Vegetation Index (SAVI) for the center of an image.
    """
    # undo the background adjustment
    region = np.where(savi == -255, 0, savi)

    # mean of center rows
    center_row1 = np.mean(region[int(multiplier * len(region))])
    center_row2 = np.mean(region[int(multiplier * len(region)) + 1])

    # mean of both rows
    mean = (center_row1 + center_row2) / 2
    return round(mean, 3)


def get_savi(red_file, nir_file, L=0.5):
    """
    This function calculates the SAVI using Red and Near Infrared (NIR) bands with a given soil brightness correction factor, L.
    """
    with rasterio.open(red_file) as band_red:
        red = band_red.read(1).astype('float64')

    with rasterio.open(nir_file) as band_nir:
        nir = band_nir.read(1).astype('float64')

    np.seterr(divide='ignore', invalid='ignore')
    # savi calculation, empty cells or nodata cells are reported as 0
    savi = np.where((nir == 0.) | (red == 0.), -255,
                    np.where((nir - red) == 0., 0, (nir - red) / (nir + red + L)) * (1 + L))

    return savi


def savi_calculator(B04, B08, saving_file_name, L=0):
    """
    This function visualizes and calculates SAVI for the provided Red and NIR bands, and returns an image.
    """
    # Open the Red band using rasterio and read the data
    with rasterio.open(B04) as src:
        band_red = src.read(1)

    # Open the NIR band using rasterio and read the data
    with rasterio.open(B08) as f:
        band_nir = f.read(1)

    # Allow division by zero
    numpy.seterr(divide='ignore', invalid='ignore')

    # Calculate SAVI
    savi = ((band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red + L)) * (1 + L)

    # Find the minimum and maximum values of SAVI
    min_value = numpy.nanmin(savi)
    max_value = numpy.nanmax(savi)

    # Create a figure and axis to visualize the SAVI
    fig, ax = plt.subplots(figsize=(75, 25))

    # Define a colormap for visualization
    cmap = 'RdYlGn'

    # Display the SAVI data
    ax.imshow(savi, cmap=cmap, clim=(min_value, max_value), vmin=min_value, vmax=max_value)

    # Turn off the axis
    ax.axis('off')

    # Save the figure to a BytesIO object
    f = BytesIO()
    fig.savefig(f, format="png", bbox_inches='tight', transparent=True, pad_inches=0)

    # Close the figure to free memory
    plt.close(fig)

    # Convert the BytesIO object to a Django ContentFile
    content_file = ContentFile(f.getvalue())

    return content_file


def average_savi(red_file, nir_file):
    """
    This function calculates the average SAVI for given Red and NIR images.
    """
    return get_region_of_interest(get_savi(red_file=red_file, nir_file=nir_file))
