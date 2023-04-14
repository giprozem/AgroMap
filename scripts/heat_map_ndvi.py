import glob
import os
from itertools import product

import geojson
import geopandas as gpd
import rasterio as rio
from osgeo import gdal, osr, ogr
from pyproj import Proj, transform
from rasterio import windows

from indexes.index_funcs.ndvi_funcs import get_ndvi, get_region_of_interest
from indexes.models.satelliteimage import SciHubImageDate
from gip.views.handbook_contour import contour_Kyrgyzstan
from indexes.index_funcs.common_funcs import cutting_tiff

import json
from shapely.geometry import GeometryCollection, Point, LineString, Polygon
from shapely.geometry import mapping
from shapely import wkt


def get_tiles(ds, width=50, height=50):
    nols, nrows = ds.meta['width'], ds.meta['height']
    offsets = product(range(0, nols, width), range(0, nrows, height))
    big_window = windows.Window(col_off=0, row_off=0, width=nols, height=nrows)
    for col_off, row_off in offsets:
        window = windows.Window(col_off=col_off, row_off=row_off, width=width, height=height).intersection(big_window)
        transform = windows.transform(window, ds.transform)
        yield window, transform


def cropping(in_path, out_path, output_filename):
    with rio.open(os.path.join(in_path)) as inds:
        tile_width, tile_height = 50, 50

        meta = inds.meta.copy()

        for window, transform in get_tiles(inds):
            meta['transform'] = transform
            meta['width'], meta['height'] = window.width, window.height
            outpath = os.path.join(out_path, output_filename.format(int(window.col_off), int(window.row_off)))
            with rio.open(outpath, 'w', **meta) as outds:
                outds.write(inds.read(window=window))


def get_epsg(ref):
    if ref.IsProjected():
        return int(ref.GetAuthorityCode("PROJCS"))
    elif ref.IsGeographic():
        return int(ref.GetAuthorityCode("GEOGCS"))


def get_center_point(file_path):
    raster = gdal.Open(file_path)
    gt = raster.GetGeoTransform()
    # get EPSG
    projection = raster.GetProjection()
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

    # return centerX, centerY
    return {'longitude': x2, 'latitude': y2}


def response_convert_shape_file(response_in_json, output_file_name, output_path):
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

    # Kонвертация GeoJson в Shpfile
    gdf = gpd.read_file(f'./{output_path}/{output_file_name}.geojson')
    gdf.to_file(f'./{output_path}/{output_file_name}.shp')
    return f'{output_file_name}.shp'


def convert_shape_to_tif(shapesile_name, output_path):
    print(f'shapesile_name === {shapesile_name}')
    pts = ogr.Open(f"{shapesile_name}", 0)
    layer = pts.GetLayer()
    # set the desired output size to 1000 x 1000 pixels
    width = 11000
    height = 11000

    pts = layer = None
    nn = gdal.Grid(f'./{output_path}/first.tif', f'{shapesile_name}', zfield='ndvi',
                   algorithm='invdist',
                   outputType=gdal.GDT_Float32,
                   width=width,
                   height=height
                   )
    nn = None


def run():
    # Create the directory if it doesn't already exist
    temporary_folder = 'heat-map'
    if not os.path.exists(f'./media/{temporary_folder}'):
        os.makedirs(f'./media/{temporary_folder}')

    images = SciHubImageDate.objects.all()
    for image in images:
        out_path = f'./media/{temporary_folder}'

        satellite_image_b04 = f'./media/{image.B04}'
        output_filename_b04 = 'tile_{}-{}_B04.tif'

        satellite_image_b8a = f'./media/{image.B8A}'
        output_filename_b8a = 'tile_{}-{}_B8A.tif'

        try:
            cropping(in_path=satellite_image_b04, out_path=out_path, output_filename=output_filename_b04)
        except Exception as e:
            print(f'error == {e}')

        try:
            cropping(in_path=satellite_image_b8a, out_path=out_path, output_filename=output_filename_b8a)
        except Exception as e:
            print(f'error == {e}')

        B8A = []
        B04 = []

        # Loop through the files in folder1
        for filename in os.listdir(out_path):
            full_path = os.path.join(out_path, filename)
            if 'B8A' in filename:
                B8A.append(filename)
            elif 'B04' in filename:
                B04.append(filename)

        B8A.sort()
        B04.sort()

        out = []
        for i in range(len(B8A)):
            fn_nir = B8A[i]
            fn_red = B04[i]
            fn_nir = f'{out_path}/{fn_nir}'
            fn_red = f'{out_path}/{fn_red}'

            response = get_region_of_interest(get_ndvi(red_file=fn_red, nir_file=fn_nir))
            response = {'ndvi': response}
            point = get_center_point(fn_red)
            point.update(response)
            out.append(point)

        # Search files with .tiff extension in current directory
        pattern = f"./media/{temporary_folder}/*.tif"
        files = glob.glob(pattern)

        # deleting the files with tiff extension
        for file in files:
            os.remove(file)

        response_convert_shape_file(response_in_json=out, output_file_name='./media/heat-map', output_path='ndvi')
        convert_shape_to_tif(shapesile_name='./media/heat-map/ndvi.shp', output_path='./media/heat-map/')

    return ''
