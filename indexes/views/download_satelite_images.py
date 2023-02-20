import os
import re
import shutil
import time
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from sentinelsat import SentinelAPI
from zipfile import ZipFile
from osgeo import gdal

from indexes.models import SciHubImageDate, SciHubAreaInterest


class DownloadAPIView(APIView):
    def get(self, request):
        output = 'output/'
        # Скачиваем снимки через Sci-hub
        api = SentinelAPI('kaiumamanbaev', 'Copernicus123!', 'https://scihub.copernicus.eu/dhus')
        footprint = SciHubAreaInterest.objects.get(pk=1).polygon.wkt
        products = api.query(footprint,
                             date=('20220901', '20220930'),
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
                                    gdal.Translate(tiff_path,  jp2_path, format='GTiff')
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
                                    sci_hub_image_date.B01.save('B01.tif', open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B02.*.tif", filename):
                                    sci_hub_image_date.B02.save('B02.tif', open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B03.*.tif", filename):
                                    sci_hub_image_date.B03.save('B03.tif', open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B04.*.tif", filename):
                                    sci_hub_image_date.B04.save('B04.tif', open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B05.*.tif", filename):
                                    sci_hub_image_date.B05.save('B05.tif', open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B06.*.tif", filename):
                                    sci_hub_image_date.B06.save('B06.tif', open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B07.*.tif", filename):
                                    sci_hub_image_date.B07.save('B07.tif', open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B08.*.tif", filename):
                                    sci_hub_image_date.B08.save('B08.tif', open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B8A.*.tif", filename):
                                    sci_hub_image_date.B8A.save('B8A.tif', open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B09.*.tif", filename):
                                    sci_hub_image_date.B09.save('B09.tif', open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B10.*.tif", filename):
                                    sci_hub_image_date.B10.save('B10.tif', open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B11.*.tif", filename):
                                    sci_hub_image_date.B11.save('B11.tif', open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B12.*.tif", filename):
                                    sci_hub_image_date.B12.save('B12.tif', open(f"{img_data_path}/{filename}", 'rb'))
                                sci_hub_image_date.save()
        except Exception as e:
            print(e)
        shutil.rmtree(output)
        return Response('OK')
