import datetime
import os
import shutil
from glob import glob
from itertools import product

import geojson
import pandas as pd
import rasterio as rio
from geopandas import GeoDataFrame
from osgeo import gdal, osr, ogr
from pyproj import Proj, transform
from rasterio import windows
from shapely.geometry import Point

from indexes.index_funcs.ndvi_funcs import get_ndvi, get_region_of_interest
from indexes.models.satelliteimage import SciHubImageDate, SciHubAreaInterest
from indexes.index_funcs.common_funcs import cutting_tiff


def get_tiles(ds, width=50, height=50):
    """
    Yields windows and transforms of the given dataset as tiles of the specified width and height.

    :param ds: Input dataset.
    :param width: Width of the tile.
    :param height: Height of the tile.
    """
    nols, nrows = ds.meta['width'], ds.meta['height']  # Width and height of the dataset
    offsets = product(range(0, nols, width), range(0, nrows, height))  # Calculate offset for each tile
    big_window = windows.Window(col_off=0, row_off=0, width=nols,
                                height=nrows)  # The window representing the whole dataset
    for col_off, row_off in offsets:
        window = windows.Window(col_off=col_off, row_off=row_off, width=width, height=height).intersection(
            big_window)  # Tile window
        transform = windows.transform(window, ds.transform)  # Transformation for the current tile
        yield window, transform


def cropping(in_path, out_path, output_filename, date):
    """
    Crop a satellite image into tiles and save them to a specified path.

    :param in_path: Path to the input satellite image.
    :param out_path: Path where the cropped images should be saved.
    :param output_filename: Filename format for the cropped images.
    :param date: Date information for the image, used in naming the cropped images.
    """
    with rio.open(os.path.join(in_path)) as inds:
        tile_width, tile_height = 50, 50  # Dimensions for tiles
        meta = inds.meta.copy()

        for window, transform in get_tiles(inds):
            meta['transform'] = transform
            meta['width'], meta['height'] = window.width, window.height  # Update metadata for cropped image
            outpath = os.path.join(out_path, output_filename.format(int(window.col_off), int(window.row_off), date))
            with rio.open(outpath, 'w', **meta) as outds:
                outds.write(inds.read(window=window))


def get_epsg(ref):
    """
    Retrieve the EPSG code from a spatial reference.

    :param ref: Spatial reference.
    :return: EPSG code.
    """
    if ref.IsProjected():
        return int(ref.GetAuthorityCode("PROJCS"))
    elif ref.IsGeographic():
        return int(ref.GetAuthorityCode("GEOGCS"))


def get_center_point(file_path):
    """
    Get the center coordinates (longitude and latitude) of a given raster file.

    :param file_path: Path to the raster file.
    :return: Dictionary containing longitude and latitude of the center point.
    """
    raster = gdal.Open(file_path)
    gt = raster.GetGeoTransform()  # Geotransform parameters
    projection = raster.GetProjection()  # Get projection
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromWkt(projection)
    epsg = get_epsg(spatial_ref)
    width = raster.RasterXSize
    height = raster.RasterYSize

    centerX = gt[0] + width * gt[1] / 2 + height * gt[2] / 2
    centerY = gt[3] + width * gt[4] / 2 + height * gt[5] / 2
    inProj = Proj(init=f'epsg:{epsg}')
    outProj = Proj(init='epsg:4326')
    x1, y1 = centerX, centerY
    x2, y2 = transform(inProj, outProj, x1, y1)

    return {'longitude': x2, 'latitude': y2}


def response_convert_shape_file(response_in_json, output_file_name, output_path):
    """
    Convert a JSON response (containing coordinates and NDVI data) to a GeoJSON format and save to a file.

    :param response_in_json: JSON response to be converted.
    :param output_file_name: Name of the output GeoJSON file.
    :param output_path: Path where the GeoJSON file should be saved.
    """
    # Convert the JSON response to GeoJSON
    my_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(d["longitude"]), float(d["latitude"]), float(d["ndvi"])],
                },
                "properties": d,
            } for d in response_in_json]
    }

    # Write the GeoJSON data to a file
    with open(f'./{output_path}/{output_file_name}.geojson', 'w') as f:
        geojson.dump(my_geojson, f)


def convert_shape_to_tif(shapesile_name, output_path, output_file_name):
    """
    Convert a shapefile to TIFF format.

    :param shapesile_name: Name of the input shapefile.
    :param output_path: Path where the TIFF file should be saved.
    :param output_file_name: Name of the output TIFF file.
    """
    pts = ogr.Open(f"{shapesile_name}", 0)
    layer = pts.GetLayer()
    width = 11000  # Desired output width
    height = 11000  # Desired output height
    algorithm_options = 'invdist:smoothing=0.01'  # Algorithm options for conversion

    pts = layer = None
    nn = gdal.Grid(f'./{output_path}/{output_file_name}.tif', f'{shapesile_name}', zfield='ndvi',
                   algorithm=algorithm_options,
                   outputType=gdal.GDT_Float32,
                   width=width,
                   height=height
                   )
    nn = None


def creating_folder(creating_folder_name):
    """
    Create a folder with a specified name, if it doesn't exist.

    :param creating_folder_name: Name of the folder to be created.
    :return: Name of the folder.
    """
    try:
        if not os.path.exists(f'./media/{creating_folder_name}'):
            os.makedirs(f'./media/{creating_folder_name}')
        return f'{creating_folder_name}'
    except:
        return f'{creating_folder_name}'


def merge_df(links):
    """
    Merge multiple CSV files into a single DataFrame.

    :param links: List of links to CSV files.
    :return: Merged DataFrame.
    """
    dataframes = []

    for i, link in enumerate(links):
        df = pd.read_csv(link)
        dataframes.append(df)

    merged_df = pd.concat(dataframes)
    return merged_df


def run(year=datetime.datetime.now().year):
    """
    This function processes satellite images of interest areas to extract and save NDVI data for a specific year.
    It crops images, calculates NDVI, merges and averages data, then converts results to various formats.
    """

    # Query all areas of interest
    areas_interested = SciHubAreaInterest.objects.all()

    # Loop through each area of interest
    for area_interested in areas_interested:

        # Filter satellite images by date for the given area of interest
        filtered = SciHubImageDate.objects.filter(
            area_interest=area_interested
        ).filter(
            date__range=(f'{year}-04-01 00:00:00', f'{year}-10-10 00:00:00')
        )

        temporary_folder = 'heat-map'  # Define temporary folder for data processing

        if filtered:
            for i in filtered:
                out = []

                # Naming the directory based on the date of the satellite image and area of interest ID
                image_dir = f'{str(i.date)[:10]}-{area_interested.id}'

                # Create necessary folders
                creating_folder(f'{temporary_folder}/{image_dir}')
                creating_folder(f'{temporary_folder}/csv')
                satellite_image = f'./media/{temporary_folder}/{image_dir}'

                # Try cropping B04 satellite band
                try:
                    cropping(
                        in_path=f'./media/{str(i.B04)}',
                        out_path=satellite_image,
                        output_filename='tile_{}-{}_B04.tif',
                        date=image_dir
                    )
                except Exception as e:
                    print(f'error == {e}')

                # Try cropping B8A satellite band
                try:
                    cropping(
                        in_path=f'./media/{str(i.B8A)}',
                        out_path=satellite_image,
                        output_filename='tile_{}-{}_B8A.tif',
                        date=image_dir
                    )
                except Exception as e:
                    print(f'error == {e}')

                B8A = []
                B04 = []

                # Loop through the files in satellite_image directory
                for filename in os.listdir(satellite_image):
                    if 'B8A' in filename:
                        B8A.append(filename)
                    elif 'B04' in filename:
                        B04.append(filename)

                # Sort filenames
                B04.sort()
                B8A.sort()

                # Calculate NDVI for each pair of B04 and B8A
                for j in range(len(B8A)):
                    fn_nir = B8A[j]
                    fn_red = B04[j]
                    fn_nir = f'{satellite_image}/{fn_nir}'
                    fn_red = f'{satellite_image}/{fn_red}'
                    response = get_region_of_interest(get_ndvi(red_file=fn_red, nir_file=fn_nir))
                    response = {'ndvi': response}
                    point = get_center_point(fn_red)
                    point.update(response)
                    out.append(point)

                # Remove temporary directory
                shutil.rmtree(f"./media/{temporary_folder}/{image_dir}")

                # Save NDVI data to a CSV file
                df = pd.DataFrame(out)
                df.to_csv(f"./media/{temporary_folder}/csv/{area_interested.id}{image_dir}.csv")

    # Merge all CSVs into a single CSV
    input_files = sorted(glob("./media/heat-map/csv/*.csv"))
    df = merge_df(input_files)
    df = df.drop(columns=['Unnamed: 0'])

    # Calculate the mean NDVI and save
    mean_ndvi = df.groupby(['longitude', 'latitude'])['ndvi'].mean().reset_index()
    mean_ndvi.to_csv('./media/heat-map/csv/grouped.csv')

    # Create a GeoDataFrame from the DataFrame
    geometry = [Point(xyz) for xyz in zip(mean_ndvi.longitude, mean_ndvi.latitude, mean_ndvi.ndvi)]
    gdf = GeoDataFrame(mean_ndvi, geometry=geometry)
    gdf.to_file('./media/heat-map/csv/result.geojson')

    # Convert geojson to tif
    convert_shape_to_tif(shapesile_name='./media/heat-map/csv/result.geojson',
                         output_path='./media/heat-map/csv/',
                         output_file_name='result')

    # Cut the resulting tif using the Kyrgyzstan contour
    cutting_tiff(
        outputpath='./media/heat-map/csv/',
        inputpath='./media/heat-map/csv/result.tif',
        polygon='KyrgyzstanContour.geojson'
    )
