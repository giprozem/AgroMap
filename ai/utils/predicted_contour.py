import time

import cv2
from django.db import connection
from osgeo import gdal
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
from ai.models.create_dataset import *


def merge_bands(instance):
    path = 'cutted/tup/'
    files = [f"{path}2022-07-26-00:00_2022-07-26-23:59_Sentinel-2_L2A_B0{i}_(Raw).tiff" for i in range(2, 5)]

    # Открываем первый файл из списка для получения метаданных
    with rasterio.open(files[0]) as src:
        meta = src.meta
        meta.update(count=len(files))  # Устанавливаем количество каналов в метаданных
        meta.update(driver="GTiff")  # Устанавливаем тип драйвера в метаданных

    # Создаем выходной файл с помощью метаданных и записываем в него данные из всех файлов
    output_file = f"media/Merge_Bands/ID=MINI_TUP_DATE=1.tif"
    with rasterio.open(output_file, "w", **meta) as dst:
        for id, layer in enumerate(files, start=1):
            with rasterio.open(layer) as src:
                dst.write(src.read(1), id)
    Merge_Bands.objects.all().delete()
    Merge_Bands.objects.create(is_passed=True, type_of_process=instance.type_of_process)


def create_rgb(instance):
    time.sleep(8)
    merge_bands_list = os.listdir('media/Merge_Bands')

    for band_rgb in merge_bands_list:
        # Открываем входной файл с помощью Rasterio
        with rasterio.open(f'media/Merge_Bands/{band_rgb}') as src:
            # Читаем каналы красного, зеленого и синего цветов
            red = src.read(3)
            green = src.read(2)
            blue = src.read(1)

            # Масштабируем значения пикселей до диапазона от 0 до 255
            red = np.interp(red, (red.min(), red.max()), (0, 255)).astype('uint8')
            green = np.interp(green, (green.min(), green.max()), (0, 255)).astype('uint8')
            blue = np.interp(blue, (blue.min(), blue.max()), (0, 255)).astype('uint8')

            # Изменяем яркость и насыщенность каждого канала
            brightness = 50
            saturation = 1.5

            red = cv2.convertScaleAbs(red, alpha=1, beta=brightness)
            red = cv2.convertScaleAbs(red, alpha=saturation)

            green = cv2.convertScaleAbs(green, alpha=1, beta=brightness)
            green = cv2.convertScaleAbs(green, alpha=saturation)

            blue = cv2.convertScaleAbs(blue, alpha=1, beta=brightness)
            blue = cv2.convertScaleAbs(blue, alpha=saturation)

            # Создаем RGB изображение, объединив каналы в одно изображение
            rgb = np.dstack((red, green, blue))

            # Получаем метаданные из исходного файла и обновляем количество каналов и тип данных
            meta = src.meta.copy()
            meta.update(count=3, dtype='uint8')

            # Записываем RGB изображение в новый файл в формате GeoTIFF
            with rasterio.open(f"media/RGB/RGB_{band_rgb}", 'w', **meta) as dst:
                dst.write(rgb.transpose(2, 0, 1))
    Create_RGB.objects.all().delete()
    Create_RGB.objects.create(is_passed=True, type_of_process=instance.type_of_process)


def cut_rgb_tif():
    time.sleep(8)
    rgb_tif_list = os.listdir('media/RGB')
    input_file = os.path.join('media/RGB', 'Bishkek.tif')
    os.makedirs('test_yolo/test', exist_ok=True)

    # Открываем входной файл с помощью GDAL
    ds = gdal.Open(input_file)
    if ds is not None:
        band = ds.GetRasterBand(1)
        xsize = band.XSize
        ysize = band.YSize

        out_path = 'test_yolo/640_Bishkek'
        output_filename = 'KG_'
        num = 1  # Переменная для хранения номера файла

        tile_size_x = 640
        tile_size_y = 640

        # Обрезаем изображение сначала так, чтобы содержать первые верхние тайлы 320px
        for i in range(0, xsize, tile_size_x):
            for j in range(0, ysize, tile_size_y):
                # Определяем границы области, которую надо вырезать
                # left = i
                # top = j
                # width = tile_size_x
                # height = tile_size_y
                #
                # # Проверяем, не выходим ли мы за границы изображения
                # if left + width > xsize:
                #     width = xsize - left
                # if top + height > ysize:
                #     height = ysize - top

                output_file = os.path.join(out_path, output_filename + str(num) + "_CENTER.tif")
                num += 1  # Увеличиваем номер файла

                # Обрезаем изображение
                dst = gdal.Translate(output_file, ds, srcWin=[i, j, tile_size_x, tile_size_y])

        # Обрезаем изображение затем так, чтобы не содержать первые верхние тайлы 320px
        for i in range(0, xsize, tile_size_x):
            for j in range(320, ysize, tile_size_y):
                # # Определяем границы области, которую надо вырезать
                # left = i
                # top = j
                # width = tile_size_x
                # height = tile_size_y
                #
                # # Проверяем, не выходим ли мы за границы изображения
                # if left + width > xsize:
                #     width = xsize - left
                # if top + height > ysize:
                #     height = ysize - top

                output_file = os.path.join(out_path, output_filename + str(num) + "_TOP.tif")
                num += 1  # Увеличиваем номер файла

                # Обрезаем изображение
                dst = gdal.Translate(output_file, ds, srcWin=[i, j, tile_size_x, tile_size_y])

            # Обрезаем изображение слева на право, чтобы не содержать первые левые тайлы 320px
        for i in range(320, xsize, tile_size_x):
            for j in range(0, ysize, tile_size_y):
                # # Определяем границы области, которую надо вырезать
                # left = i
                # top = j
                # width = tile_size_x
                # height = tile_size_y
                #
                # # Проверяем, не выходим ли мы за границы изображения
                # if left + width > xsize:
                #     width = xsize - left
                # if top + height > ysize:
                #     height = ysize - top

                output_file = os.path.join(out_path, output_filename + str(num) + "_LEFT.tif")
                num += 1  # Увеличиваем номер файла

                # Обрезаем изображение
                dst = gdal.Translate(output_file, ds, srcWin=[i, j, tile_size_x, tile_size_y])

        # Освобождаем ресурсы
        ds = None
        dst = None
    else:
        print(f"Не удалось открыть файл: Bishkek.tif")


def yolo():
    # from datetime import date
    # year = date.today().strftime("%Y")
    file_yolo = Yolo.objects.get(id=1)
    model = YOLO(f'media/{file_yolo.ai}')
    cutted_files = sorted(os.listdir('media/TCI/'),
                          key=lambda x: int(x.split('_')[1].split('.')[0].replace('KG_', '')))

    for file in cutted_files:
        print(file, '--------------------')
        image = Image.open(f'media/TCI/{file}')
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
            arrays = results[0].masks.xyn
            confs = results[0].boxes.conf
            if arrays is not None:
                w, h = image.size
                x = 1 / w
                y = 1 / h
                # img = Image.fromarray(results[0].orig_img)
                # plt.imshow(img)
                for i in arrays:
                    df = pd.DataFrame(i)
                    df.loc[len(df)] = ([i[0][0], i[0][1]])
                    plt.plot(df[0] / x, df[1] / y, c="red")
                plt.axis('off')
                with rasterio.open(f'media/TCI/{file}') as src:
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
                        # Создать геометрию полигона из столбцов координат
                        polygon = shp.Polygon(zip(coords[:, 1], coords[:, 0]))
                        # polygon

                        # Сгладить углы полигона
                        smooth_polygon = polygon.simplify(0.0001, preserve_topology=True)
                        # smooth_polygon

                        # Получить координаты полигона
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
                                    Contour_AI.objects.create(polygon=poly, percent=round(float(conf), 2), year='2022',
                                                              type_id=1)
                                except Exception as e:
                                    print(e, '------------ Save contour')
                        except Exception as e:
                            print(e, '--------------Intesection')
                            try:
                                Contour_AI.objects.create(polygon=poly, percent=round(float(conf), 2), year='2022',
                                                          type_id=1)
                            except Exception as e:
                                print(e, '=============== Exept Exception')
        except Exception as e:
            print(e)
            print(file, '=======================')
            try:
                image = Image.open(f'media/BANDS/{file}')
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
                    img = Image.fromarray(results[0].orig_img)
                    # plt.imshow(img)
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
                            # Создать геометрию полигона из столбцов координат
                            polygon = shp.Polygon(zip(coords[:, 1], coords[:, 0]))
                            # polygon

                            # Сгладить углы полигона
                            smooth_polygon = polygon.simplify(0.0001, preserve_topology=True)
                            # smooth_polygon

                            # Получить координаты полигона
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
                                        print(e, '------------ Save contour')
                            except Exception as e:
                                print(e, '--------------Intesection')
                                try:
                                    Contour_AI.objects.create(polygon=poly, percent=round(float(conf), 2), year='2022',
                                                              type_id=1)
                                except Exception as e:
                                    print(e, '=============== Exept Exception')
            except Exception as e:
                print(e)


def clean_contour_and_create_district():
    model_contour = Contour_AI.objects.all().order_by('id')
    for i in model_contour:
        id_contour = i.id
        area_ha = i.area_ha
        polygon = i.polygon
        try:
            print(id_contour, '---------------')
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
                print(id_contour, '================')
                print(polygon)
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
                    print(cursor.fetchall())
                    print(district)
                    Contour_AI.objects.filter(id=id_contour).update(district_id=district)
            except Exception as e:
                print(e, 'TOPOLOGY')

        try:
            if area_ha is None:
                print(area_ha, 'area_ha is NONE')
                ha = round(polygon.area / 10 ** (-6), 2)
                Contour_AI.objects.filter(id=id_contour).update(area_ha=float(ha))  # 73544
            if area_ha < 1.0:
                print(area_ha, 'area_ha DELETE')
                Contour_AI.objects.filter(id=id_contour).delete()
            if area_ha > 70.0:
                print(area_ha, 'area_ha DELETE')
                Contour_AI.objects.filter(id=id_contour).delete()
        except Exception as e:
            print(e)


def deleted_files():
    time.sleep(8)
    merge_bands_dir = "media/Merge_Bands"
    rgb_dir = "media/RGB"
    cut_tif_dir = 'media/cutted_tiff'

    # Удаление файлов в директории Merge_bands
    for file_name in os.listdir(merge_bands_dir):
        file_path = os.path.join(merge_bands_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Удаление файлов в директории RGB
    for file_name in os.listdir(rgb_dir):
        file_path = os.path.join(rgb_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Удаление файлов в директории cutted_tiff
    for file_name in os.listdir(cut_tif_dir):
        file_path = os.path.join(cut_tif_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    Process.objects.filter(id=1).update(is_running=False)
