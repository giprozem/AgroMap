from io import BytesIO

import matplotlib.pyplot as plt
import numpy
import numpy as np
import rasterio
from osgeo import gdal


def cutting_tiff(outputpath, inputpath, polygon):

    gdal.Warp(destNameOrDestDS=outputpath,
              srcDSOrSrcDSTab=inputpath,
              cutlineDSName=polygon,
              cropToCutline=True,
              copyMetadata=True,
              dstNodata=0)


def get_region_of_interest(ndvi, multiplier=1/2):

    # undo the background adjustment
    region = ndvi.copy()
    region = np.where(region == -255, 0, region)

    # mean of center rows
    center_row1 = np.mean(region[int((multiplier) *len(region))])
    center_row2 = np.mean(region[int((multiplier) *len(region))+1])

    # mean of both rows
    mean = (center_row1.copy()+center_row2.copy())/2
    return mean


def get_ndvi(red_file, nir_file):
    band_red = rasterio.open(red_file)
    band_nir = rasterio.open(nir_file)
    red = band_red.read(1).astype('float64')
    nir = band_nir.read(1).astype('float64')

    np.seterr(divide='ignore', invalid='ignore')
    # ndvi calculation, empty cells or nodata cells are reported as 0
    ndvi=np.where( (nir==0.) | (red ==0.), -255 , np.where((nir+red)==0., 0, (nir-red)/(nir+red)))

    return ndvi


def ndvi_calculator(B04, B8A, saving_file_name):

    with rasterio.open(f'{B04}') as src:
        band_red = src.read(1)

    with rasterio.open(f'{B8A}') as f:
        band_nir = f.read(1)

    # Allow division by zero
    numpy.seterr(divide='ignore', invalid='ignore')

    # # Calculate NDVI
    ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)

    min_value = numpy.nanmin(ndvi)
    max_value = numpy.nanmax(ndvi)
    mid = 0.1

    fig = plt.figure(figsize=(75, 25))
    ax = fig.add_subplot(111)

    cmap = plt.cm.YlGn
    cax = ax.imshow(ndvi, cmap=cmap, clim=(min_value, max_value), vmin=min_value, vmax=max_value)

    ax.axis('off')

    f = BytesIO()

    plt.savefig(f'./media/{saving_file_name}.png', format='png', transparent=True, bbox_inches='tight')


def average_ndvi(red_file, nir_file):
    return get_region_of_interest(get_ndvi(red_file=red_file, nir_file=nir_file))
