import matplotlib.pyplot as plt
import numpy
import numpy as np
import rasterio


def get_region_of_interest(ndmi, multiplier=1/2):

    # undo the background adjustment
    region = ndmi.copy()
    region = np.where(region == -255, 0, region)

    # mean of center rows
    center_row1 = np.mean(region[int((multiplier) *len(region))])
    center_row2 = np.mean(region[int((multiplier) *len(region))+1])

    # mean of both rows
    mean = (center_row1.copy()+center_row2.copy())/2
    return mean


def get_ndmi(swir_file, nir_file):
    band_swir = rasterio.open(swir_file)
    band_nir = rasterio.open(nir_file)
    swir = band_swir.read(1).astype('float64')
    nir = band_nir.read(1).astype('float64')

    np.seterr(divide='ignore', invalid='ignore')
    # ndwi calculation, empty cells or nodata cells are reported as 0
    ndmi = np.where((nir == 0.) | (swir == 0.), -255, np.where((nir+swir) == 0., 0, (nir - swir)/(nir + swir)))

    return ndmi


def ndmi_calculator(B08, B11, saving_file_name):

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

    plt.savefig(f'./media/{saving_file_name}.png', format='png', transparent=True, bbox_inches='tight')


def average_ndmi(swir_file, nir_file):
    return get_region_of_interest(get_ndmi(swir_file=swir_file, nir_file=nir_file))
