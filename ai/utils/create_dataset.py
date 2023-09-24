from datetime import date
import shutil
import os
from rasterio import warp
import rasterio
from ai.models.create_dataset import Dataset
from django.contrib.gis.geos import Polygon
from django.db import connection
from PIL import Image
from pyproj import Proj, Transformer
from pyproj.transformer import transform as trnsfrm


def create_dataset():

    """
    This function was created to create a dataset that can be used to train machine learning models, 
    namely for object detection tasks in images.
    """

    cutted_files = os.listdir('media/cutted_tiff')

    for file in cutted_files:
        # Open the raster file using rasterio
        with rasterio.open(f'media/cutted_tiff/{file}') as src:
            # Get the bounding box in the original CRS (Coordinate Reference System)
            bbox_m = src.bounds
            # Transform the bounding box to EPSG:4326 (WGS84) CRS
            bbox = warp.transform_bounds(src.crs, {'init': 'EPSG:4326'}, *bbox_m)
            # Create a Shapely Polygon from the bounding box coordinates
            bboxs = Polygon.from_bbox(bbox)
            # Open a database connection cursor
            with connection.cursor() as cursor:
                # Execute a SQL query to retrieve GeoJSON polygons that are properly contained within the bounding box
                cursor.execute(f"""
                SELECT St_AsGeoJSON(cntr.polygon) AS polygon
                FROM ai_contour_ai AS cntr
                where cntr.is_deleted=false and 
                ST_ContainsProperly('{bboxs}'::geography::geometry, cntr.polygon::geometry);
                """)
                # Fetch the query results
                rows = cursor.fetchall()
                data = []
                # Convert the GeoJSON data to a list              
                for i in rows:
                    data.append(eval(i[0]))
                # Initialize label string
                label = ''
                image = Image.open(f'media/cutted_tiff/{file}')
                w, h = image.size
                # Save the image as a PNG in the training dataset directory
                image.save(f'media/dataset/train/images/{file[:-4]}.png')
                for c in data:
                    coordinates = c['coordinates'][0]
                    meters = []
                    for i in range(0, len(coordinates)):
                        inProj = Proj(init='epsg:4326')
                        outProj = Proj(init=f'epsg:{src.crs.to_epsg()}')
                        x1, y1 = coordinates[i][0], coordinates[i][1]
                        x2, y2 = trnsfrm(inProj, outProj, x1, y1)
                        meters.append([x2, y2])
                    xs = []
                    ys = []
                    for i in meters:
                        xs.append(i[0])
                        ys.append(i[1])
                    y, x = rasterio.transform.rowcol(src.transform, xs, ys)
                    txt = '0 '
                    for i in range(0, len(x)):
                        txt += f'{x[i] / w} {y[i] / h} '
                    label += f'{txt}\n'
        with open(f"media/dataset/train/labels/{file[:-4]}.txt", "w") as txt_file:
            txt_file.write(label)
    # Create a ZIP archive of the dataset directory
    shutil.make_archive('dataset', 'zip', root_dir='media/dataset')
    obj = Dataset.objects.create()
    name = date.today().strftime("%d-%m-%Y")
    obj.zip.save(name, open('./dataset.zip', 'rb'))
    # Remove the temporary ZIP archive file
    os.remove('./dataset.zip')
