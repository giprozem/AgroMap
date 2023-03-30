import random
import time
from datetime import datetime

from django.db import connection
from osgeo import gdal, osr
import os

from gip.views.handbook_contour import contour_test_for_ai, contour_Chui_2
from indexes.models.satelliteimage import SciHubImageDate
import rasterio
import numpy as np
from ai.models import Contour_AI, Images_AI, Yolo
from ultralytics import YOLO
from PIL import Image
from pyproj import Proj, Transformer
from pyproj.transformer import transform as trnsfrm
from django.contrib.gis.geos import GEOSGeometry
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Polygon


def merge_bands():
    # Фильтруем объекты SciHubImageDate по ID и загружаем изображения
    satellite_images = SciHubImageDate.objects.filter(id__in=[154, 155])

    for image in satellite_images:
        time.sleep(2)
        path = 'media/'
        files = [
            path + f"{image.B02}",  # Синий
            path + f"{image.B03}",  # Зеленый
            path + f"{image.B04}",  # Красный
        ]

        # Открываем первый файл из списка для получения метаданных
        with rasterio.open(files[0]) as src:
            meta = src.meta
            meta.update(count=len(files))  # Устанавливаем количество каналов в метаданных
            meta.update(driver="GTiff")  # Устанавливаем тип драйвера в метаданных

        # Создаем выходной файл с помощью метаданных и записываем в него данные из всех файлов
        output_file = f"media/Merge_Bands/ID={image.pk}_DATE={datetime.fromisoformat(str(image.date)).strftime('%Y-%m-%d')}.tif"
        with rasterio.open(output_file, "w", **meta) as dst:
            for id, layer in enumerate(files, start=1):
                with rasterio.open(layer) as src:
                    dst.write(src.read(1), id)


def create_rgb():
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

            # Создаем RGB изображение, объединив каналы в одно изображение
            rgb = np.dstack((red, green, blue))

            # Получаем метаданные из исходного файла и обновляем количество каналов и тип данных
            meta = src.meta.copy()
            meta.update(count=3, dtype='uint8')

            # Записываем RGB изображение в новый файл в формате GeoTIFF
            with rasterio.open(f"media/RGB/RGB_{band_rgb}", 'w', **meta) as dst:
                dst.write(rgb.transpose(2, 0, 1))


def cut_rgb_tif():
    time.sleep(8)
    rgb_tif_list = os.listdir('media/RGB')
    for rgb_tif in rgb_tif_list:
        input_file = os.path.join('media/RGB', rgb_tif)

        # Открываем входной файл с помощью GDAL
        ds = gdal.Open(input_file)
        if ds is not None:
            band = ds.GetRasterBand(1)
            xsize = band.XSize
            ysize = band.YSize

            out_path = 'media/cutted_tiff/'
            output_filename = f"tile_"

            tile_size_x = 256
            tile_size_y = 256

            # Обрезаем изображение на тайлы
            for i in range(0, xsize, tile_size_x):
                for j in range(0, ysize, tile_size_y):
                    output_file = os.path.join(out_path,
                                               output_filename + str(i) + "_" + f"{random.randint(1, 10000)}" + str(
                                                   j) + f"{random.randint(1, 10000)}" + ".tif")
                    com_string = f"gdal_translate -of GTIFF -srcwin {i}, {j}, {tile_size_x}, {tile_size_y} {input_file} {output_file}"
                    os.system(com_string)

        else:
            print(f"Не удалось открыть файл: {rgb_tif}")


def yolo():
    file_yolo = Yolo.objects.get(id=1)
    model = YOLO(f'media/{file_yolo.ai}')
    cutted_files = os.listdir('media/cutted_tiff')

    for file in cutted_files:
        ds = gdal.Open(f"media/cutted_tiff/{file}", gdal.GA_ReadOnly)

        proj = osr.SpatialReference(wkt=ds.GetProjection())
        proj_wgs84 = osr.SpatialReference()
        proj_wgs84.ImportFromEPSG(4326)
        transform = osr.CoordinateTransformation(proj, proj_wgs84)

        ulx, xres, xskew, uly, yskew, yres = ds.GetGeoTransform()
        lrx = ulx + (ds.RasterXSize * xres)
        lry = uly + (ds.RasterYSize * yres)

        ul_lon, ul_lat, _ = transform.TransformPoint(ulx, uly)
        lr_lon, lr_lat, _ = transform.TransformPoint(lrx, lry)

        coords = [
            [[ul_lat, ul_lon, ], [ul_lat, lr_lon], [lr_lat, lr_lon], [lr_lat, ul_lon],
             [ul_lat, ul_lon]]]
        geojson = {
            "type": "Polygon",
            "coordinates": coords
        }

        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT ST_Intersects('{contour_Chui_2}'::geography::geometry, '{GEOSGeometry(f"{geojson}")}'::geography::geometry);
            """)
            inside = cursor.fetchall()
        if inside[0][0] == True:
            image = Image.open(f'media/cutted_tiff/{file}')
            results = model.predict(source=image, save=False, conf=0.05, hide_labels=True, line_thickness=1)
            try:
                arrays = results[0].masks.segments
                confs = results[0].boxes.conf
                w, h = image.size
                x = 1 / w
                y = 1 / h
                img = Image.fromarray(results[0].orig_img)
                plt.imshow(img)
                for i in arrays:
                    df = pd.DataFrame(i)
                    df.loc[len(df)] = ([i[0][0], i[0][1]])
                    plt.plot(df[0] / x, df[1] / y, c="red")
                plt.axis('off')
                plt.savefig(f'media/images/{file[:-4]}.png', transparent=True, bbox_inches='tight', pad_inches=0)
                images = Images_AI.objects.create()
                images.image.save(os.listdir('media/images/')[0],
                                  open(f"media/images/{os.listdir('media/images')[0]}", 'rb'))
                with rasterio.open(f'media/cutted_tiff/{file}') as src:
                    for n in range(0, len(arrays)):
                        coordinates = []
                        for i in arrays[n]:
                            coordinates.append(src.xy(i[1] / x, i[0] / y))
                        coordinates.append(coordinates[0])
                        geojsons = []
                        for i in range(0, len(coordinates)):
                            inProj = Proj(init=f'epsg:{src.crs.to_epsg()}')
                            outProj = Proj(init='epsg:4326')
                            x1, y1 = coordinates[i][0], coordinates[i][1]
                            x2, y2 = trnsfrm(inProj, outProj, x1, y1)
                            geojsons.append([x2, y2])
                        conf = confs[n]
                        coords = np.array(geojsons)

                        # Создать геометрию полигона из столбцов координат
                        polygon = Polygon(zip(coords[:, 0], coords[:, 1]))
                        # polygon

                        # Сгладить углы полигона
                        smooth_polygon = polygon.simplify(0.0001, preserve_topology=True)
                        # smooth_polygon

                        # Получить координаты полигона
                        vertices = list(smooth_polygon.exterior.coords)
                        list_of_values = [list(tuple) for tuple in vertices]

                        print(round(float(conf), 1), '------------------------------')
                        geojson = {
                            "type": "Polygon",
                            "coordinates": [list_of_values]
                        }
                        poly = GEOSGeometry(f"{geojson}")

                    # with connection.cursor() as cursor:
                    #     cursor.execute(f"""
                    #         SELECT ST_Contains('{contour_Chui_2}'::geography::geometry, '{poly}'::geography::geometry);
                    #     """)
                    #     inside_contour = cursor.fetchall()[0][0]
                    #     if inside_contour == True:
                    #     with connection.cursor() as cursor:
                    #         cursor.execute(f"""
                    #         SELECT SUM(subquery.percent) as total_percent
                    #         FROM (
                    #             SELECT ST_Area(ST_Intersection(scm.polygon::geometry,
                    #             '{poly}'::geography::geometry)) / ST_Area(scm.polygon::geometry) * 100 as percent
                    #             FROM ai_contour_ai as scm
                    #         ) as subquery;
                    #         """)
                    #         # percent = cursor.fetchall()[0][0]
                    #         percent = cursor.fetchall()[0][0]
                    #         print(percent)
                    #     if round(percent) < 30 or percent == None:
                        with connection.cursor() as cursor:
                            cursor.execute(f"""
                            SELECT dst.id FROM gip_district AS dst WHERE ST_Contains(dst.polygon::geography::geometry,
                            '{poly}'::geography::geometry);
                            """)
                            district = cursor.fetchall()[0][0]
                        Contour_AI.objects.create(polygon=poly, percent=round(float(conf), 1), district_id=district)
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


"""
<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">
  <sld:NamedLayer>
    <sld:Name>style_agromap</sld:Name>
    <sld:Title>Countries Mapcolor9</sld:Title>
    <sld:Abstract>Theme using mapcolor9 for ne:countries layer.</sld:Abstract>
    <sld:UserStyle>
      <sld:Name />
      <sld:FeatureTypeStyle>
        <sld:Rule>
          <sld:Name>agromap_store</sld:Name>
        </sld:Rule>
        <sld:Rule>
          <sld:PolygonSymbolizer>
            <sld:Fill>
              <sld:CssParameter name="fill">
                <ogc:Function name="Recode">
                  <ogc:PropertyName>prdvty</ogc:PropertyName>
                  <ogc:Literal>1</ogc:Literal>
                  <ogc:Literal>#1BA87D</ogc:Literal>
                  <ogc:Literal>0</ogc:Literal>
                  <ogc:Literal>#b3ec84</ogc:Literal>
                </ogc:Function>
              </sld:CssParameter>
            </sld:Fill>
            <Stroke>
              <CssParameter name="stroke">#000000</CssParameter>
              <CssParameter name="stroke-width">0.25</CssParameter>
            </Stroke>
          </sld:PolygonSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>

"""

"""
SELECT ST_Contains('GEOMETRYCOLLECTION(POLYGON ((73.113236 42.130944, 73.109537 42.141426, 73.089367 42.15535, 73.11503 42.160267, 73.112627 42.173165, 73.100611 42.181385, 73.070656 42.182678, 73.046173 42.194937, 73.057459 42.21755, 73.05452 42.263188, 73.08868 42.258278, 73.100814 42.24959, 73.116607 42.254437, 73.12622 42.269738, 73.130168 42.298673, 73.160037 42.313581, 73.178062 42.29931, 73.239173 42.318168, 73.260202 42.30874, 73.268184 42.298354, 73.294019 42.296889, 73.30655 42.285864, 73.324231 42.290771, 73.347277 42.287266, 73.356718 42.311447, 73.418216 42.312562, 73.429202 42.301604, 73.451175 42.313008, 73.496665 42.288796, 73.524903 42.308103, 73.53486 42.306064, 73.553571 42.317531, 73.590135 42.319951, 73.611936 42.333326, 73.608503 42.372543, 73.616448 42.386778, 73.623829 42.38856, 73.633013 42.421573, 73.659106 42.444208, 73.621855 42.458923, 73.603187 42.448753, 73.590313 42.449389, 73.579155 42.462863, 73.55392 42.468583, 73.553234 42.445448, 73.538986 42.438582, 73.532634 42.424975, 73.519073 42.416835, 73.499886 42.429333, 73.485793 42.41285, 73.475789 42.46563, 73.44327 42.50194, 73.42467 42.54704, 73.42787 42.64064, 73.43987 42.65724, 73.466442 42.731469, 73.501271 42.767136, 73.508246 42.797939, 73.509653 42.868352, 73.505078 42.885563, 73.493923 42.894092, 73.499453 42.907515, 73.492353 42.915313, 73.509322 42.93161, 73.534363 42.943959, 73.54846 42.966731, 73.538644 42.974926, 73.535475 43.006995, 73.545264 43.027259, 73.691086 43.073109, 73.763886 43.106844, 73.794219 43.112714, 73.828076 43.128961, 73.83806 43.117665, 73.905437 43.109604, 73.928345 43.146632, 73.948231 43.164328, 73.958521 43.199272, 73.953603 43.207568, 73.969532 43.222838, 74.042391 43.17187, 74.074866 43.186814, 74.156047 43.197037, 74.211446 43.195097, 74.222117 43.205312, 74.192888 43.255523, 74.200519 43.266691, 74.205222 43.262573, 74.21044 43.265362, 74.206145 43.25866, 74.214482 43.262843, 74.229088 43.250568, 74.251294 43.253222, 74.244242 43.247119, 74.255863 43.248907, 74.262075 43.242636, 74.286006 43.245446, 74.280008 43.242528, 74.295914 43.239367, 74.289846 43.235619, 74.302376 43.230523, 74.293201 43.228376, 74.302878 43.226883, 74.305622 43.215071, 74.317117 43.21827, 74.319835 43.212347, 74.332314 43.218835, 74.330165 43.212311, 74.340527 43.210422, 74.340487 43.201428, 74.347764 43.204903, 74.360616 43.194799, 74.383778 43.196943, 74.390534 43.192907, 74.387525 43.188785, 74.398827 43.191129, 74.40416 43.186638, 74.397272 43.182944, 74.406536 43.172179, 74.410975 43.175271, 74.414489 43.168646, 74.424322 43.172479, 74.420031 43.165482, 74.441955 43.156736, 74.448439 43.159365, 74.454441 43.15386, 74.459452 43.158775, 74.458793 43.151947, 74.468106 43.153261, 74.472054 43.142962, 74.479505 43.155361, 74.495998 43.156617, 74.497672 43.143388, 74.531563 43.141264, 74.535928 43.134615, 74.550487 43.138371, 74.563973 43.134809, 74.564032 43.128252, 74.58203 43.128739, 74.583566 43.116151, 74.59996 43.108673, 74.596352 43.103317, 74.616355 43.082668, 74.631607 43.079853, 74.639026 43.062272, 74.66198 43.052593, 74.671849 43.04085, 74.695523 43.036504, 74.72775 43.003266, 74.750062 42.989371, 74.762716 42.993811, 74.775694 42.990431, 74.782834 42.999542, 74.800435 42.995079, 74.813497 43.001251, 74.853323 42.999595, 74.872558 42.99321, 74.879605 42.982978, 74.895929 42.980514, 74.90454 42.970522, 74.920102 42.970122, 74.920459 42.961955, 74.937018 42.963441, 74.970567 42.941057, 74.980797 42.945183, 75.037847 42.918481, 75.050329 42.922401, 75.071728 42.912523, 75.08167 42.91412, 75.136735 42.885203, 75.187479 42.874634, 75.195028 42.865047, 75.226511 42.85277, 75.261421 42.860256, 75.296773 42.860342, 75.318578 42.852481, 75.369266 42.848937, 75.459886 42.831173, 75.488558 42.84154, 75.513566 42.832045, 75.567832 42.82831, 75.60828 42.814504, 75.635181 42.81519, 75.672944 42.801303, 75.713534 42.796171, 75.755339 42.828565, 75.778343 42.837242, 75.796184 42.909984, 75.821821 42.936083, 75.86227 42.95014, 75.89587 42.94304, 75.92717 42.95454, 75.96077 42.93384, 76.00647 42.93024, 76.02277 42.91394, 76.03547 42.90994, 76.13437 42.92354, 76.26847 42.91924, 76.29967 42.90564, 76.31547 42.87094, 76.32317 42.86604, 76.34707 42.86554, 76.44487 42.88594, 76.48547 42.88894, 76.51407 42.91874, 76.56647 42.90964, 76.60737 42.91274, 76.72327 42.90524, 76.73907 42.91484, 76.75547 42.94594, 76.80267 42.95104, 76.84627 42.98264, 76.85967 42.98514, 76.897133 42.96619, 76.907062 42.971601, 76.917363 42.966197, 76.938904 42.981978, 76.956779 42.979476, 76.973342 42.988011, 76.984182 42.980455, 77.000917 42.984759, 77.019192 42.966309, 77.020616 42.955975, 77.034014 42.954396, 77.033833 42.947774, 77.05148 42.955801, 77.061844 42.97721, 77.084642 42.981201, 77.124683 42.969643, 77.152106 42.973109, 77.160174 42.943858, 77.188419 42.942508, 77.226779 42.924522, 77.208383 42.903348, 77.200744 42.907323, 77.182291 42.90196, 77.178428 42.893693, 77.134235 42.873859, 77.120502 42.82681, 77.096985 42.809181, 77.031582 42.816132, 76.998108 42.806527, 76.965149 42.808802, 76.920345 42.80362, 76.900604 42.807412, 76.884124 42.801092, 76.888845 42.782665, 76.880863 42.78042, 76.856315 42.793633, 76.837347 42.794328, 76.810739 42.788007, 76.786621 42.77473, 76.716497 42.773276, 76.696756 42.77884, 76.578138 42.763744, 76.561465 42.772297, 76.51443 42.766732, 76.475806 42.785195, 76.457267 42.754273, 76.429629 42.751869, 76.404824 42.73947, 76.385684 42.740103, 76.380105 42.745101, 76.365342 42.7327, 76.351094 42.729536, 76.340623 42.714854, 76.3238 42.715487, 76.313672 42.70422, 76.307149 42.705739, 76.261487 42.676487, 76.248784 42.675094, 76.237798 42.653683, 76.195483 42.641835, 76.195359 42.624208, 76.182656 42.610135, 76.153817 42.607218, 76.140599 42.614066, 76.10558 42.617679, 76.089615 42.609121, 76.055112 42.608233, 76.041293 42.598532, 76.010308 42.604429, 75.964346 42.580615, 75.919568 42.586446, 75.879752 42.572101, 75.863785 42.580937, 75.835139 42.585883, 75.815558 42.600473, 75.80406 42.582181, 75.818378 42.558723, 75.811169 42.545758, 75.816693 42.532529, 75.810071 42.528487, 75.779962 42.539812, 75.759547 42.536332, 75.745611 42.521496, 75.70803 42.518944, 75.689394 42.478199, 75.671455 42.464093, 75.652272 42.457451, 75.641428 42.445012, 75.632759 42.448381, 75.619885 42.435285, 75.597483 42.433314, 75.580145 42.421232, 75.552679 42.420342, 75.547959 42.429308, 75.533882 42.425493, 75.521952 42.432742, 75.522038 42.445202, 75.514399 42.449716, 75.49071 42.435348, 75.480667 42.437764, 75.444382 42.429357, 75.424899 42.435969, 75.408848 42.424524, 75.376318 42.450082, 75.349024 42.431391, 75.308512 42.429802, 75.281304 42.416702, 75.267142 42.421408, 75.25701 42.415834, 75.236754 42.430269, 75.213923 42.429125, 75.196671 42.435292, 75.182509 42.427599, 75.16045 42.425055, 75.124315 42.443176, 75.109123 42.44432, 75.078053 42.421176, 75.008616 42.426899, 75.002865 42.435229, 74.963554 42.423656, 74.916176 42.43561, 74.90313 42.426963, 74.876436 42.430333, 74.852833 42.421939, 74.802536 42.420222, 74.79979 42.406548, 74.83086 42.367862, 74.850172 42.357996, 74.854549 42.331254, 74.876093 42.317815, 74.858326 42.304245, 74.840902 42.299658, 74.835066 42.305774, 74.82305 42.301697, 74.786486 42.306029, 74.765972 42.292202, 74.736103 42.295835, 74.720825 42.274102, 74.695162 42.26862, 74.690012 42.244072, 74.679369 42.233675, 74.660658 42.243498, 74.634737 42.244518, 74.587273 42.237247, 74.570622 42.229529, 74.559979 42.234313, 74.526419 42.229912, 74.49243 42.21677, 74.473118 42.225319, 74.462217 42.222066, 74.450716 42.225829, 74.443592 42.219833, 74.428743 42.222767, 74.417843 42.215749, 74.411663 42.218142, 74.398274 42.201743, 74.392265 42.174423, 74.358448 42.149519, 74.376644 42.140832, 74.392609 42.122816, 74.34935 42.081524, 74.352955 42.04961, 74.325371 42.045626, 74.324512 42.034493, 74.314556 42.03027, 74.313784 42.018943, 74.319454 42.016737, 74.314647 41.999965, 74.268258 41.973204, 74.266541 41.946811, 74.274094 41.934507, 74.268429 41.926239, 74.245856 41.9122, 74.205 41.924252, 74.191182 41.920662, 74.181998 41.924636, 74.158223 41.911431, 74.137452 41.884626, 74.133714 41.854295, 74.123007 41.842744, 74.111656 41.85853, 74.130839 41.917182, 74.126505 41.925484, 74.101536 41.912406, 74.061023 41.903109, 74.028494 41.941474, 73.982317 41.961592, 73.96467 41.981567, 73.952997 41.979582, 73.919265 41.955497, 73.887251 41.959405, 73.862961 41.954985, 73.845537 41.967541, 73.814209 41.949475, 73.792665 41.944284, 73.783224 41.9587, 73.78743 41.969526, 73.772066 41.976828, 73.761122 42.008683, 73.725589 42.002889, 73.703768 42.012686, 73.696 42.007709, 73.683769 42.015262, 73.654437 42.009677, 73.638064 42.000267, 73.608131 41.999995, 73.598947 41.993784, 73.55513 42.002673, 73.526384 41.994511, 73.493768 42.00962, 73.467483 42.005699, 73.443879 42.021765, 73.415963 42.013988, 73.41276 42.027828, 73.393556 42.023629, 73.383546 42.033026, 73.34938 42.021999, 73.337525 42.028238, 73.336415 42.054466, 73.318605 42.068825, 73.323283 42.077778, 73.3091 42.093857, 73.147566 42.121691, 73.129198 42.118241, 73.113236 42.130944), (74.465114 42.857882, 74.486385 42.860437, 74.489066 42.853196, 74.489084 42.860104, 74.509433 42.862242, 74.510419 42.855382, 74.490859 42.85542, 74.498902 42.851736, 74.493758 42.82048, 74.510909 42.825496, 74.535364 42.850657, 74.528969 42.838495, 74.538402 42.836368, 74.537774 42.809358, 74.545184 42.813901, 74.555489 42.811909, 74.577869 42.786532, 74.586523 42.786599, 74.592484 42.802505, 74.612222 42.80285, 74.612819 42.80691, 74.645709 42.801307, 74.639375 42.832345, 74.651924 42.83439, 74.651948 42.840827, 74.705019 42.845489, 74.701642 42.866839, 74.718968 42.866119, 74.69747 42.872451, 74.696728 42.878254, 74.656365 42.881052, 74.650979 42.90922, 74.644202 42.910155, 74.646549 42.893214, 74.631744 42.894826, 74.626219 42.929042, 74.637946 42.948665, 74.617262 42.94881, 74.631341 42.966817, 74.626643 42.972686, 74.621084 42.964539, 74.614913 42.967681, 74.613099 42.960426, 74.60766 42.961737, 74.610824 42.929384, 74.60475 42.912853, 74.596381 42.911805, 74.599192 42.930118, 74.593125 42.930473, 74.600008 42.940681, 74.592606 42.952584, 74.598822 42.967742, 74.584429 42.972629, 74.560309 42.967334, 74.575981 42.947113, 74.590619 42.950467, 74.575749 42.927405, 74.577477 42.911923, 74.557476 42.909435, 74.55586 42.895788, 74.509715 42.893244, 74.51238 42.874127, 74.500656 42.874992, 74.502213 42.863748, 74.477487 42.862704, 74.465374 42.868883, 74.465114 42.857882)))'::geography::geometry, 'POLYGON ((73.87177924970138 42.79966450519947, 73.87177924970138 42.76921384641375, 73.91016789046063 42.76921384641375, 73.91016789046063 42.79966450519947, 73.87177924970138 42.79966450519947))'::geography::geometry);

"""


def create_dataset():
    data = []
    coordinates = Contour_AI.objects.filter(image_id=4)
    for i in coordinates:
        data.append(i.polygon.wkt)
    label = ''
    for line in data:
        line = line.replace('POLYGON ', '').removesuffix('))').removeprefix('((')
        line = line.split(', ')
        coordinates = []
        for j in line:
            j = j.split(' ')
            coordinates.append([float(j[0]), float(j[1])])
        image = Image.open('media/cutted_tiff/tile_0_20546084632.tif')
        w, h = image.size
        image.save('media/dataset/images/tile_0_20546084632.png')
        with rasterio.open('media/cutted_tiff/tile_0_20546084632.tif') as src:
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

    with open("media/dataset/labels/tile_0_20546084632.txt", "w") as txt_file:
        txt_file.write(label)
