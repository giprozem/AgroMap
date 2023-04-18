import io
import os
import re
import shutil
import time
from datetime import datetime

from PIL import Image
import rasterio
from rest_framework.response import Response
from sentinelsat import SentinelAPI
from zipfile import ZipFile
from osgeo import gdal
from datetime import date

from indexes.models import SciHubImageDate, SciHubAreaInterest
from decouple import config

"""
*/10 * * * * docker exec plot_web_1 ./manage.py runscript cron_download_S2_Copernicus -v3
"""

SCI_HUB_USERNAME = config('SCI_HUB_USERNAME')
SCI_HUB_PASSWORD = config('SCI_HUB_PASSWORD')


def run():
    current_date = date.today()
    first_day_of_previous_month = date(current_date.year, current_date.month - 1, 1)

    output = 'output/'

    # Скачиваем снимки через Sci-hub
    api = SentinelAPI(SCI_HUB_USERNAME, SCI_HUB_PASSWORD, 'https://scihub.copernicus.eu/dhus')

    # Define a list of footprints
    footprints = [sci_hub_area_interest for sci_hub_area_interest in
                  SciHubAreaInterest.objects.all()]

    for footprint in footprints:
        print(current_date.strftime("%Y%m%d"))
        print(first_day_of_previous_month.strftime("%Y%m%d"))
        products = api.query(footprint,
                             date=(first_day_of_previous_month.strftime("%Y%m%d"), current_date.strftime("%Y%m%d")),
                             platformname='Sentinel-2',
                             processinglevel='Level-2A',
                             cloudcoverpercentage=(0, 20))

        if len(products) > 1:
            tiff_coords = []
            for i in products.keys():
                metadata_product = api.get_product_odata(i)
                check_len_coordinates = len(metadata_product['footprint'].strip("POLYGON((").strip("))").split(","))
                if check_len_coordinates == 5:
                    tiff_coords.append(metadata_product['footprint'])
                    api.download(products[i]['uuid'], directory_path=output)
                    break
        else:
            SciHubImageDate.objects.create(area_interest_id=footprint.pk, no_image=True,
                                           note=f'Не удалось получить ни один продукт '
                                                f'({first_day_of_previous_month.strftime("%Y.%m.%d")}-'
                                                f'{current_date.strftime("%Y.%m.%d")})')
            continue

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

                # Tiff сохраняем в базу данных
                img_date = datetime.strptime(os.path.basename(folder)[11:19], '%Y%m%d')
                sci_hub_image_date = SciHubImageDate(date=img_date, area_interest_id=footprint.pk)
                if folder.endswith('.SAFE'):
                    for file in os.listdir(os.path.join(output, folder, 'GRANULE')):
                        if file.startswith('L2A_'):
                            img_data_path = os.path.join(output, folder, 'GRANULE', file, 'IMG_DATA', 'R20m')
                            for filename in os.listdir(img_data_path):
                                if re.search(".*B01.*.tif", filename):
                                    sci_hub_image_date.B01.save('B01.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B02.*.tif", filename):
                                    print(f"{img_data_path}/{filename}")
                                    with rasterio.open(f"{img_data_path}/{filename}") as geotiff_image:
                                        # Считываем данные о масштабе и размерах изображения
                                        scale = geotiff_image.read(1).max()

                                        # Читаем изображение в массив numpy
                                        image_array = geotiff_image.read(1)

                                        # Нормализуем значения пикселей до диапазона 0-255
                                        image_array = (image_array / scale * 255).astype('uint8')

                                        # Создаем изображение PIL из массива numpy
                                        png_image = Image.fromarray(image_array, 'L')

                                        # Преобразуем изображение в байты
                                        img_bytes = io.BytesIO()
                                        png_image.save(img_bytes, format='PNG')
                                        img_bytes.seek(0)

                                        # Создаем экземпляр модели изображения
                                    sci_hub_image_date.polygon = tiff_coords[0]
                                    sci_hub_image_date.B02.save('B02.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                    sci_hub_image_date.image_png.save('image.png', img_bytes, save=True)
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
