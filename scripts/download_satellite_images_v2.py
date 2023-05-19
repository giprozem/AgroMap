import io
import os
import re
import shutil
import time
from datetime import datetime
from zipfile import ZipFile

import rasterio
import requests
from PIL import Image
from decouple import config
from osgeo import gdal
from rest_framework.response import Response
from indexes.models import SciHubAreaInterest
from indexes.models import SciHubImageDate


def run():
    SCI_HUB_USERNAME_V2 = config('SCI_HUB_USERNAME_V2')
    SCI_HUB_PASSWORD_V2 = config('SCI_HUB_PASSWORD_V2')

    # Устанавливаем путь к папке output
    output = 'output_satellite_images_script/'

    footprints = [sci_hub_area_interest for sci_hub_area_interest in SciHubAreaInterest.objects.all().order_by('id')]

    for footprint in footprints:
        dates = ['2020-04-01, 2020-04-30', '2020-05-01, 2020-05-30', '2020-06-01, 2020-06-30', '2020-07-01, 2020-07-30',
                 '2020-08-01, 2020-08-30', '2020-09-01, 2020-09-30', '2020-10-01, 2020-10-30',
                 '2021-04-01, 2021-04-30', '2021-05-01, 2021-05-30', '2021-06-01, 2021-06-30', '2021-07-01, 2021-07-30',
                 '2021-08-01, 2021-08-30', '2021-09-01, 2021-09-30', '2021-10-01, 2021-10-30',
                 '2022-04-01, 2022-04-30', '2022-05-01, 2022-05-30', '2022-06-01, 2022-06-30', '2022-07-01, 2022-07-30',
                 '2022-08-01, 2022-08-30', '2022-09-01, 2022-09-30', '2022-10-01, 2022-10-30',
                 ]
        time.sleep(15)
        for date in dates:
            os.makedirs(output, exist_ok=True)

            data = {
                "client_id": "cdse-public",
                "username": SCI_HUB_USERNAME_V2,
                "password": SCI_HUB_PASSWORD_V2,
                "grant_type": "password",
            }
            try:
                response_token = requests.post(
                    "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
                    data=data)
                response_token.raise_for_status()
            except Exception as e:
                raise Exception(
                    f"Keycloak token creation failed. Reponse from the server was: {response_token.json()}"
                )

            url = 'https://catalogue.dataspace.copernicus.eu/odata/v1/Products'
            params = {
                '$filter': f"""OData.CSC.Intersects(area=geography'SRID=4326;{footprint.polygon.wkt}') 
                        and ContentDate/Start gt {date[:10]}T00:00:00.000Z and 
                        ContentDate/Start lt {date[12:]}T00:00:00.000Z and 
                        Collection/Name eq 'SENTINEL-2' and 
                        Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and 
                        att/OData.CSC.DoubleAttribute/Value lt 20.00) and contains(Name,'S2A_MSIL2A')""",
                '$orderby': 'ContentDate/Start'
            }

            products = requests.get(url, params=params).json()['value']
            if len(products) > 1:
                # Получаем координаты TIFF-файла
                tiff_coords = []
                for product in products:
                    check_online_true = product['Online']
                    check_len_coordinates = len(product['Footprint'].strip("POLYGON((").strip("))").split(","))
                    if check_online_true and check_len_coordinates == 5:
                        tiff_coords.append(product['Footprint'].strip("geography'"))
                        print(date[:10], date[12:])
                        headers = {'Authorization': f'Bearer {response_token.json()["access_token"]}'}
                        response_download = requests.get(f"{url}({product['Id']})/$value", headers=headers)
                        with open(f"{output}{product['Name']}.zip", 'wb') as f:
                            f.write(response_download.content)
                        break
                    elif not check_online_true and check_len_coordinates != 5:
                        print(date[:10], date[12:], '-------------------', footprint.pk)
                        SciHubImageDate.objects.create(area_interest_id=footprint.pk, no_image=True,
                                                       polygon=product['Footprint'].strip("geography'"),
                                                       note=f'Не удалось получить ни один продукт ({date})')
                        break

            # Разархивируем файлы
            time.sleep(10)
            for file in os.listdir(output):
                print('ZIP')
                if file.endswith('.zip'):
                    with ZipFile(f"{output}{file}") as zipObj:
                        zipObj.extractall(output)

            # Конвертируем jp2 в tiff и сохраняем в базу данных
            time.sleep(20)
            try:
                for folder in os.listdir(output):
                    if folder.endswith('.SAFE'):
                        for file in os.listdir(os.path.join(output, folder, 'GRANULE')):
                            if file.startswith('L2A_'):
                                img_data_path = os.path.join(output, folder, 'GRANULE', file, 'IMG_DATA',
                                                             'R10m')
                                for filename in os.listdir(img_data_path):
                                    if re.search(".*B.*", filename):
                                        jp2_path = os.path.join(img_data_path, filename)
                                        tiff_path = os.path.join(img_data_path, filename[:-3] + 'tif')
                                        gdal.Translate(tiff_path, jp2_path, format='GTiff')
                                    elif re.search(".*TCI.*", filename):
                                        jp2_path = os.path.join(img_data_path, filename)
                                        tiff_path = os.path.join(img_data_path, filename[:-3] + 'tif')
                                        gdal.Translate(tiff_path, jp2_path, format='GTiff')

                    # Tiff сохраняем в базу данных
                    if folder.endswith('.SAFE'):
                        img_date = datetime.strptime(os.path.basename(folder)[11:19], '%Y%m%d')
                        sci_hub_image_date = SciHubImageDate(date=img_date, area_interest_id=footprint.pk)
                        sci_hub_image_date.name_product = folder
                        for file in os.listdir(os.path.join(output, folder, 'GRANULE')):
                            if file.startswith('L2A_'):
                                img_data_path = os.path.join(output, folder, 'GRANULE', file, 'IMG_DATA',
                                                             'R10m')
                                for filename in os.listdir(img_data_path):
                                    if re.search(".*B02.*.tif", filename):
                                        # Создаем экземпляр модели изображения
                                        sci_hub_image_date.polygon = tiff_coords[0]
                                        sci_hub_image_date.B02.save(f'B02_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*TCI.*.tif", filename):
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
                                        sci_hub_image_date.TCI.save(f'TCI_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                        sci_hub_image_date.image_png.save('image.png', img_bytes, save=True)
                                    elif re.search(".*B03.*.tif", filename):
                                        sci_hub_image_date.B03.save(f'B03_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*B04.*.tif", filename):
                                        sci_hub_image_date.B04.save(f'B04_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))

                                    elif re.search(".*B08.*.tif", filename):
                                        sci_hub_image_date.B8A.save(f'B08_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    sci_hub_image_date.save()
                time.sleep(15)
                shutil.rmtree(output)
            except Exception as e:
                print(e)
    return Response('OK')
