import os
import re
import shutil
import time
from datetime import datetime

import rasterio
from pyproj import Proj, transform
from django.contrib.gis.geos import GEOSGeometry
from pyproj import transform
from rest_framework.response import Response
from rest_framework.views import APIView
from sentinelsat import SentinelAPI
from zipfile import ZipFile
from osgeo import gdal

from indexes.models import SciHubImageDate, SciHubAreaInterest


class DownloadAPIView(APIView):
    def get(self, request):

        # start_date = request.GET.get('start_date')
        # end_date = request.GET.get('end_date')

        output = 'output/'

        inProj = Proj(init='epsg:28473')
        outProj = Proj(init='epsg:4326')

        # Скачиваем снимки через Sci-hub
        api = SentinelAPI('kaiumamanbaev', 'Copernicus123!', 'https://scihub.copernicus.eu/dhus')

        date = {
            'start_date': ['20220901', '20221001', '20221101', '20221201',  '20230101', '20230201'],
            'end_date': ['20220930', '20221030', '20221130', '20221230',  '20230130', '20230227']
        }

        # Define a list of footprints
        footprints = [sci_hub_area_interest.polygon.wkt for sci_hub_area_interest in
                      SciHubAreaInterest.objects.all()]

        for i in range(len(date['start_date'])):
            start_date = date['start_date'][i]
            end_date = date['end_date'][i]
            print(f"{start_date}--------{end_date}")
            for footprint in footprints:
                print(footprint)
                products = api.query(footprint,
                                     date=(start_date, end_date),
                                     platformname='Sentinel-2',
                                     processinglevel='Level-2A',
                                     cloudcoverpercentage=(0, 20))

                if len(products) >= 1:
                    product_id = list(products.keys())[0]  # Получаем идентификатор продукта
                    api.download(product_id, directory_path=output)
                else:
                    print("Не удалось получить ни один продукт")

                # Разархивируем файлы
                time.sleep(10)
                print('ZIP')
                for file in os.listdir(output):
                    if file.endswith('.zip'):
                        with ZipFile(f"{output}{file}") as zipObj:
                            zipObj.extractall(output)

                # Конвертируем jp2 в tiff и сохраняем в базу данных
                time.sleep(40)
                try:
                    for folder in os.listdir(output):
                        if folder.endswith('.SAFE'):
                            for file in os.listdir(os.path.join(output, folder, 'GRANULE')):
                                if file.startswith('L2A_'):
                                    img_data_path = os.path.join(output, folder, 'GRANULE', file, 'IMG_DATA', 'R20m')
                                    for filename in os.listdir(img_data_path):
                                        if re.search(".*B.*", filename):
                                            jp2_path = os.path.join(img_data_path, filename)
                                            tiff_path = os.path.join(img_data_path, filename[:-3] + 'tif')
                                            gdal.Translate(tiff_path, jp2_path, format='GTiff')
                        time.sleep(50)
                        # Tiff сохраняем в базу данных
                        img_date = datetime.strptime(os.path.basename(folder)[11:19], '%Y%m%d')
                        sci_hub_image_date = SciHubImageDate(date=img_date, area_interest_id=1)
                        if folder.endswith('.SAFE'):
                            for file in os.listdir(os.path.join(output, folder, 'GRANULE')):
                                if file.startswith('L2A_'):
                                    img_data_path = os.path.join(output, folder, 'GRANULE', file, 'IMG_DATA', 'R20m')
                                    for filename in os.listdir(img_data_path):
                                        if re.search(".*B01.*.tif", filename):
                                            sci_hub_image_date.B01.save('B01.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        elif re.search(".*B02.*.tif", filename):
                                            # Извлечение координат из Geotiff
                                            with rasterio.open(f"{img_data_path}/{filename}") as src:
                                                geometry = [[
                                                    [src.bounds.left, src.bounds.bottom],
                                                    [src.bounds.left, src.bounds.top],
                                                    [src.bounds.right, src.bounds.top],
                                                    [src.bounds.right, src.bounds.bottom],
                                                    [src.bounds.left, src.bounds.bottom]
                                                ]]

                                                coords = []
                                                # Перевод с метровых координат в формате epsg:4326
                                                for i in range(len(geometry[0])):
                                                    x1, y1 = geometry[0][i][0], geometry[0][i][1]
                                                    x2, y2 = transform(inProj, outProj, x1, y1)
                                                    coords.append([x2, y2])

                                                coords.append(coords[0])
                                                geojson = {
                                                    "type": "Polygon",
                                                    "coordinates": [coords]
                                                }
                                                sci_hub_image_date.polygon = GEOSGeometry(f"{geojson}")
                                            sci_hub_image_date.B02.save('B02.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        elif re.search(".*B03.*.tif", filename):
                                            sci_hub_image_date.B03.save('B03.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        elif re.search(".*B04.*.tif", filename):
                                            sci_hub_image_date.B04.save('B04.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        elif re.search(".*B05.*.tif", filename):
                                            sci_hub_image_date.B05.save('B05.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        elif re.search(".*B06.*.tif", filename):
                                            sci_hub_image_date.B06.save('B06.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        elif re.search(".*B07.*.tif", filename):
                                            sci_hub_image_date.B07.save('B07.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        elif re.search(".*B08.*.tif", filename):
                                            sci_hub_image_date.B08.save('B08.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        elif re.search(".*B8A.*.tif", filename):
                                            sci_hub_image_date.B8A.save('B8A.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        elif re.search(".*B09.*.tif", filename):
                                            sci_hub_image_date.B09.save('B09.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        elif re.search(".*B10.*.tif", filename):
                                            sci_hub_image_date.B10.save('B10.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        elif re.search(".*B11.*.tif", filename):
                                            sci_hub_image_date.B11.save('B11.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        elif re.search(".*B12.*.tif", filename):
                                            sci_hub_image_date.B12.save('B12.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        sci_hub_image_date.save()
                except Exception as e:
                    print(e)
                shutil.rmtree(output)
        return Response('OK')
