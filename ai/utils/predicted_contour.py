from django.db import connection
import os

from django.contrib.gis.geos import GEOSGeometry
from shapely import geometry as shp
from ai.models import Yolo, Contour_AI
from ultralytics import YOLO
from PIL import Image
from pyproj import Proj, Transformer
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import rasterio


def predicted_contour():
    # Fetch the YOLO model from the database
    file_yolo = Yolo.objects.get(id=1)
    # Initialize the YOLO model
    model = YOLO(f'media/{file_yolo.ai}')
    # Retrieve and sort the files in the directory
    files = sorted(os.listdir(f'media/TCI/'),
                   key=lambda x: int(x.split('_')[1].split('.')[0].replace('KG_', '')))

    # Iterate over each file
    for file in files:
        # Open the image
        image = Image.open(f'media/TCI/{file}')
        # Predict using the YOLO model
        results = model.predict(source=image, half=False,
                                save=False,
                                conf=0.01,
                                boxes=False,
                                show_labels=False,
                                agnostic_nms=True,
                                retina_masks=True,
                                max_det=10000,
                                iou=0.3,
                                imgsz=640,
                                classes=1)
        try:
            # Extract masks and confidences from results
            arrays = results[0].masks.xyn
            confs = results[0].boxes.conf
            # If arrays are present
            if arrays is not None:
                w, h = image.size
                x = 1 / w
                y = 1 / h
                # Plotting the polygons
                for i in arrays:
                    df = pd.DataFrame(i)
                    df.loc[len(df)] = ([i[0][0], i[0][1]])
                    plt.plot(df[0] / x, df[1] / y, c="red")
                plt.axis('off')
                # Open the raster image
                with rasterio.open(f'media/TCI/{file}') as src:
                    # Loop over the masks
                    for n in range(0, len(arrays)):
                        coordinates = []
                        for i in arrays[n]:
                            # Convert pixel coordinates to physical coordinates
                            coordinates.append(src.xy(i[1] / x, i[0] / y))
                        # Close the polygon
                        coordinates.append(coordinates[0])
                        # Initialize the geojson
                        geojsons = []
                        # Loop over the coordinates
                        for i in range(0, len(coordinates)):
                            # Convert EPSG: to latitude and longitude
                            inProj = Proj(f'EPSG:{src.crs.to_epsg()}')
                            outProj = Proj('EPSG:4326')
                            x1, y1 = coordinates[i][0], coordinates[i][1]
                            transformer = Transformer.from_proj(inProj, outProj)
                            x2, y2 = transformer.transform(x1, y1)
                            # Add to geojson
                            geojsons.append([y2, x2])
                        # Get the confidence of the current mask
                        conf = confs[n]
                        # Create a polygon from the geojson
                        coords = np.array(geojsons)
                        polygon = shp.Polygon(zip(coords[:, 1], coords[:, 0]))

                        # Simplify the polygon
                        smooth_polygon = polygon.simplify(0.0001, preserve_topology=True)

                        # Get the vertices of the polygon
                        vertices = list(smooth_polygon.exterior.coords)
                        list_of_values = [list(tuple) for tuple in vertices]
                        # Create the final geojson
                        geojson = {
                            "type": "Polygon",
                            "coordinates": [list_of_values]
                        }
                        try:
                            # Create a GEOSGeometry object from the geojson
                            poly = GEOSGeometry(f"{geojson}")
                            # Open a database connection
                            with connection.cursor() as cursor:
                                # Execute a raw SQL query to find the intersection area
                                cursor.execute(f"""
                                SELECT SUM(subquery.percent) as total_percent
                                FROM (
                                    SELECT ST_Area(ST_Intersection(scm.polygon::geometry, '{poly}'::geography::geometry)) /
                                           NULLIF(ST_Area(scm.polygon::geometry), 0) * 100 as percent
                                    FROM ai_contour_ai as scm
                                    WHERE ST_Area(scm.polygon::geometry) <> 0
                                ) as subquery;
                                """)
                                # Fetch the results
                                percent_contour = cursor.fetchall()[0][0]
                            # If the intersection is less than 30%
                            if int(percent_contour) < 30:
                                try:
                                    # Create a new Contour_AI object in the database
                                    Contour_AI.objects.create(polygon=poly, percent=round(float(conf), 2), year='2022',
                                                              type_id=1)
                                except Exception as e:
                                    print(e)
                        except Exception as e:
                            try:
                                # If there's an error, try to create the Contour_AI object again
                                Contour_AI.objects.create(polygon=poly, percent=round(float(conf), 2), year='2022',
                                                          type_id=1)
                            except Exception as e:
                                print(e)
            # Clear the results to save memory
            del results
        except Exception as e:
            try:
                # If there's an error, try to process the image again with a different path
                image = Image.open(f'media/BANDS/{file}')
                # The rest of the code is essentially the same as above
                results = model.predict(source=image, half=False,
                                        save=False,
                                        conf=0.01,
                                        boxes=False,
                                        show_labels=False,
                                        agnostic_nms=True,
                                        retina_masks=True,
                                        max_det=10000,
                                        iou=0.3,
                                        imgsz=640,
                                        classes=1)
                arrays = results[0].masks.xyn
                if arrays is not None:
                    w, h = image.size
                    x = 1 / w
                    y = 1 / h
                    for i in arrays:
                        df = pd.DataFrame(i)
                        df.loc[len(df)] = ([i[0][0], i[0][1]])
                        plt.plot(df[0] / x, df[1] / y, c="red")
                    plt.axis('off')
                    with rasterio.open(f'media/BANDS/{file}') as src:
                        for n in range(0, len(arrays)):
                            coordinates = []
                            for i in arrays[n]:
                                coordinates.append(src.xy(i[1] / x, i[0] / y))
                            coordinates.append(coordinates[0])
                            geojsons = []
                            for i in range(0, len(coordinates)):
                                inProj = Proj(f'EPSG:{src.crs.to_epsg()}')
                                outProj = Proj('EPSG:4326')
                                x1, y1 = coordinates[i][0], coordinates[i][1]
                                transformer = Transformer.from_proj(inProj, outProj)
                                x2, y2 = transformer.transform(x1, y1)
                                geojsons.append([y2, x2])
                            conf = confs[n]
                            coords = np.array(geojsons)
                            polygon = shp.Polygon(zip(coords[:, 1], coords[:, 0]))
                            # polygon

                            smooth_polygon = polygon.simplify(0.0001, preserve_topology=True)
                            # smooth_polygon

                            vertices = list(smooth_polygon.exterior.coords)
                            list_of_values = [list(tuple) for tuple in vertices]
                            geojson = {
                                "type": "Polygon",
                                "coordinates": [list_of_values]
                            }
                            try:
                                poly = GEOSGeometry(f"{geojson}")

                                with connection.cursor() as cursor:
                                    cursor.execute(f"""
                                    SELECT SUM(subquery.percent) as total_percent
                                    FROM (
                                        SELECT ST_Area(ST_Intersection(scm.polygon::geometry, '{poly}'::geography::geometry)) /
                                               NULLIF(ST_Area(scm.polygon::geometry), 0) * 100 as percent
                                        FROM ai_contour_ai as scm
                                        WHERE ST_Area(scm.polygon::geometry) <> 0
                                    ) as subquery;
                                    """)
                                    percent_contour = cursor.fetchall()[0][0]
                                if int(percent_contour) < 30:
                                    try:
                                        Contour_AI.objects.create(polygon=poly, percent=round(float(conf), 2),
                                                                  year='2022',
                                                                  type_id=1)
                                    except Exception as e:
                                        print(e)
                            except Exception as e:
                                print(e)
                                try:
                                    Contour_AI.objects.create(polygon=poly, percent=round(float(conf), 2), year='2022',
                                                              type_id=1)
                                except Exception as e:
                                    print(e)
            except Exception as e:
                print(e)


def clean_contour_and_create_district():
    model_contour = Contour_AI.objects.all().order_by('id')
    for i in model_contour:
        id_contour = i.id
        area_ha = i.area_ha
        polygon = i.polygon
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                SELECT dst.id
                FROM gip_district AS dst
                WHERE ST_Intersects(dst.polygon::geography::geometry,
                                    '{polygon}'::geography::geometry) LiMIT 1;
                """)
                district = cursor.fetchall()[0][0]
                Contour_AI.objects.filter(id=id_contour).update(district_id=district)
        except Exception as e:

            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"""
                    SELECT dst.id
                                FROM gip_district AS dst
                                WHERE ST_Intersects(
                                    ST_MakeValid(dst.polygon::geometry),
                                    ST_MakeValid(ST_GeomFromText('{polygon}'))
                                ) LIMIT 1;
                    """)
                    district = cursor.fetchall()[0][0] if cursor.fetchall() else None
                    Contour_AI.objects.filter(id=id_contour).update(district_id=district)
            except Exception as e:
                print(e, 'TOPOLOGY')

        try:
            if area_ha is None:
                ha = round(polygon.area / 10 ** (-6), 2)
                Contour_AI.objects.filter(id=id_contour).update(area_ha=float(ha))
            if area_ha < 1.0:
                Contour_AI.objects.filter(id=id_contour).delete()
            if area_ha > 70.0:
                Contour_AI.objects.filter(id=id_contour).delete()
        except Exception as e:
            print(e)
