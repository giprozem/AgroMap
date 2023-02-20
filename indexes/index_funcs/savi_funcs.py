from io import BytesIO

import matplotlib.pyplot as plt
import numpy
import numpy as np
import rasterio


def get_region_of_interest(savi, multiplier=1/2):

    # undo the background adjustment
    region = np.where(savi == -255, 0, savi)

    # mean of center rows
    center_row1 = np.mean(region[int(multiplier * len(region))])
    center_row2 = np.mean(region[int(multiplier * len(region)) + 1])

    # mean of both rows
    mean = (center_row1 + center_row2) / 2
    return round(mean, 3)


def get_savi(red_file, nir_file, L=0.5):
    with rasterio.open(red_file) as band_red:
        red = band_red.read(1).astype('float64')

    with rasterio.open(nir_file) as band_nir:
        nir = band_nir.read(1).astype('float64')

    np.seterr(divide='ignore', invalid='ignore')
    # savi calculation, empty cells or nodata cells are reported as 0
    savi = np.where((nir == 0.) | (red == 0.), -255, np.where((nir - red) == 0., 0, (nir - red) / (nir + red + L)) * (1 + L))

    return savi


def savi_calculator(B04, B08, saving_file_name, L=0):

    with rasterio.open(f'{B04}') as src:
        band_red = src.read(1)

    with rasterio.open(f'{B08}') as f:
        band_nir = f.read(1)

    # Allow division by zero
    numpy.seterr(divide='ignore', invalid='ignore')

    # # Calculate savi
    savi = ((band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red + L)) * (1 + L)

    min_value = numpy.nanmin(savi)
    max_value = numpy.nanmax(savi)
    mid = 0.1

    fig = plt.figure(figsize=(75, 25))
    ax = fig.add_subplot(111)

    cmap = 'RdYlGn'
    cax = ax.imshow(savi, cmap=cmap, clim=(min_value, max_value), vmin=min_value, vmax=max_value)

    ax.axis('off')

    f = BytesIO()

    plt.savefig(f'./media/{saving_file_name}.png', format='png', transparent=True, bbox_inches='tight')
    plt.close()


def average_savi(red_file, nir_file):
    return get_region_of_interest(get_savi(red_file=red_file, nir_file=nir_file))
