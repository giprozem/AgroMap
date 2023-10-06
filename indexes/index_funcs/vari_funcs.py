from io import BytesIO

import matplotlib.pyplot as plt
import numpy
import numpy as np
import rasterio
from django.core.files.base import ContentFile


def get_region_of_interest(vari, multiplier=1 / 2):
    """
    This function calculates the mean value of the Visible Atmospherically Resistant Index (VARI) for the center of an image.
    """
    # undo the background adjustment
    region = np.where(vari == -255, 0, vari)

    # mean of center rows
    center_row1 = np.mean(region[int(multiplier * len(region))])
    center_row2 = np.mean(region[int(multiplier * len(region)) + 1])

    # mean of both rows
    mean = (center_row1 + center_row2) / 2
    return round(mean, 3)


def get_vari(red_file, green_file, blue_file):
    """
    This function calculates the VARI using Red, Green, and Blue bands.
    """
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
    """
    This function visualizes and calculates VARI for the provided Blue, Green, and Red bands, and returns an image.
    """
    # Open the Blue, Green, and Red bands using rasterio and read the data
    with rasterio.open(B02) as blue:
        band_blue = blue.read(1)

    with rasterio.open(B03) as green:
        band_green = green.read(1)

    with rasterio.open(B04) as red:
        band_red = red.read(1)

    # Allow division by zero
    numpy.seterr(divide='ignore', invalid='ignore')

    # Calculate VARI
    vari = ((band_green.astype(float) - band_red.astype(float)) / (band_green + band_red - band_blue))

    # Find the minimum and maximum values of VARI
    min_value = numpy.nanmin(vari)
    max_value = numpy.nanmax(vari)

    # Create a figure and axis to visualize the VARI
    fig, ax = plt.subplots(figsize=(75, 25))

    # Define a colormap for visualization
    cmap = 'RdYlGn'

    # Display the VARI data
    ax.imshow(vari, cmap=cmap, clim=(min_value, max_value), vmin=min_value, vmax=max_value)

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


def average_vari(red_file, green_file, blue_file):
    """
    This function calculates the average VARI for given Red, Green, and Blue images.
    """
    return get_region_of_interest(get_vari(red_file=red_file, green_file=green_file, blue_file=blue_file))
