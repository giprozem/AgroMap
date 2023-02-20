# from sentinelsat import SentinelAPI
# from django.contrib.gis.geos import GEOSGeometry
# from zipfile import ZipFile
# import os
# from osgeo import gdal
#
# import config
# from indexes.models import SciHubAreaInterest
#
# # Получить геометрию полигона из объекта SciHubAreaInterest
# area_of_interest = SciHubAreaInterest.objects.get(pk=1)
# geom = area_of_interest.polygon
#
# # Инициализировать API sci-hub
# api = SentinelAPI('kaiumamanbaev', 'Copernicus123!', 'https://scihub.copernicus.eu/dhus')
#
# # Запросить снимки с помощью API sci-hub
# products = api.query(geom.wkt, date=('20220901', '20220930'), platformname='Sentinel-2',
#                      processinglevel='Level-2A', cloudcoverpercentage=(0, 30))
#
# # Скачать снимки и разархивировать их
# for product_id in products:
#     product_info = api.get_product_odata(product_id)
#     print(product_info)
#     # product_name = product_info['title']
#     # zip_path = api.download(product_id, directory_path='/path/to/download/directory')
#     # with ZipFile(zip_path, 'r') as zip_file:
#     #     zip_file.extractall('/path/to/unzip/directory')
#     # os.remove(zip_path)
#     #
#     # # Конвертировать все файлы jp2 в tiff
#     # img_data_dir = '/path/to/unzip/directory/{}/GRANULE/*/IMG_DATA'.format(product_name)
#     # for jp2_file in os.listdir(img_data_dir):
#     #     jp2_path = os.path.join(img_data_dir, jp2_file)
#     #     tiff_path = os.path.splitext(jp2_path)[0] + '.tif'
#     #     gdal.Translate(tiff_path, jp2_path, format='GTiff')
#     #
#     # # Сохранить все tiff-файлы в базу данных
#     # image_date = SciHubImageDate.objects.create(area_interest=area_of_interest, date=product_info['beginposition'])
#     # for band in range(1, 13):
#     #     tiff_path = os.path.join(img_data_dir, 'B{:02d}.tif'.format(band))
#     #     if os.path.exists(tiff_path


import os
import re
from datetime import datetime
from glob import glob
from rest_framework.response import Response
from rest_framework.views import APIView
from sentinelsat import SentinelAPI
from zipfile import ZipFile
from osgeo import gdal
from django.contrib.gis.geos import GEOSGeometry

from indexes.models import SciHubImageDate, SciHubAreaInterest

output = 'output/'
output_tiff = 'output/tiff'


class DownloadAPIView(APIView):
    def get(self, request):
        # # Скачиваем снимки через Sci-hub
        # api = SentinelAPI('kaiumamanbaev', 'Copernicus123!', 'https://scihub.copernicus.eu/dhus')
        # footprint = SciHubAreaInterest.objects.get(pk=1).polygon.wkt
        # products = api.query(footprint,
        #                      date=('20220901', '20220930'),
        #                      platformname='Sentinel-2',
        #                      processinglevel='Level-2A',
        #                      cloudcoverpercentage=(0, 20))
        #
        # if len(products) >= 1:
        #     product_id = list(products.keys())[0]  # Получаем идентификатор продукта
        #     api.download(product_id, directory_path=output)
        # else:
        #     print("Не удалось получить один продукт, получено:", len(products))
        #
        # # Разархивируем файлы
        # for file in os.listdir(output):
        #     if file.endswith('.zip'):
        #         with ZipFile(f"{output}{file}") as zipObj:
        #             zipObj.extractall(output)

        # Конвертируем jp2 в tiff и сохраняем в базу данных
        for folder in os.listdir(output):
            if folder.endswith('.SAFE'):
                for file in os.listdir(os.path.join(output, folder, 'GRANULE')):
                    if file.startswith('L2A_'):
                        img_data_path = os.path.join(output, folder, 'GRANULE', file, 'IMG_DATA', 'R20m')
                        for filename in os.listdir(img_data_path):
                            if re.search(".*B.*", filename):
                                jp2_path = os.path.join(img_data_path, filename)
                                tiff_path = os.path.join(img_data_path, filename[:-3] + 'tif')
                                # gdal.Translate(tiff_path,  jp2_path, format='GTiff')

                                if re.search(".*B.*.tif", filename):
                                    img_date = datetime.strptime(os.path.basename(folder)[11:19], '%Y%m%d')
                                    print(img_date)
                                    img_path = os.path.abspath(tiff_path)
                                    print(img_path)
                                    sci_hub_image_date = SciHubImageDate(date=img_date, band=img_band, path=img_path)
                                    sci_hub_image_date.save()
                                # my_obj = SciHubImageDate.objects.create(area_interest=1,
                                #                                         B01=f)

                                # tiff_file = open(tiff_path, 'rb')
                                # image_date = SciHubImageDate(area_interest=1,
                                #                              date=datetime.strptime(file[11:26], '%Y%m%dT%H%M%S'),
                                #                              polygon=footprint.polygon)
                                # setattr(image_date, '', tiff_file)
                                # image_date.save()
        return Response('OKS')
