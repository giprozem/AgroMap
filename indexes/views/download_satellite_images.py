import io
import os
import re
import shutil
import time
import zipfile
from datetime import datetime
from threading import Thread
from zipfile import ZipFile

import rasterio
import requests
from PIL import Image
from decouple import config
from django.http import JsonResponse
from osgeo import gdal
from rest_framework.response import Response
from rest_framework.views import APIView

from indexes.models import SciHubAreaInterest
from indexes.models import SciHubImageDate


def download():
    # Конфигурационные данные SciHub
    # SCI_HUB_USERNAME_V2 = 'copernicus.sd@gmail.com'
    # SCI_HUB_PASSWORD_V2 = '!!!12345Copernicus'
    SCI_HUB_USERNAME_V2 = config('SCI_HUB_USERNAME_V2')
    SCI_HUB_PASSWORD_V2 = config('SCI_HUB_PASSWORD_V2')
    proxies = {
        'http': 'http://3.229.73.118:8888',
        'https': 'http://5.161.189.211:8080',
    }

    output = 'output_satellite_images_script/'
    footprints = [sci_hub_area_interest for sci_hub_area_interest in
                  SciHubAreaInterest.objects.all().exclude(id__in=[1, 2, 3]).order_by('id')]

    for footprint in footprints:
        print(footprint.pk)
        dates = ['2020-08-01, 2020-08-30',
                 '2020-09-01, 2020-09-30', '2020-10-01, 2020-10-30', '2020-11-01, 2020-11-30', '2020-12-01, 2020-12-30',
                 '2021-01-01, 2021-01-30', '2021-02-01, 2021-02-25', '2021-03-01, 2021-03-30', '2021-04-01, 2021-04-30',
                 '2021-05-01, 2021-05-30', '2021-06-01, 2021-06-30', '2021-07-01, 2021-07-30', '2021-08-01, 2021-08-30',
                 '2021-09-01, 2021-09-30', '2021-10-01, 2021-10-30', '2021-11-01, 2021-11-30', '2021-12-01, 2021-12-30',
                 '2022-01-01, 2022-01-30', '2022-02-01, 2022-02-25', '2022-03-01, 2022-03-30', '2022-04-01, 2022-04-30',
                 '2022-05-01, 2022-05-30', '2022-06-01, 2022-06-30', '2022-07-01, 2022-07-30', '2022-08-01, 2022-08-30',
                 '2022-09-01, 2022-09-30', '2022-10-01, 2022-10-30', '2022-11-01, 2022-11-30', '2022-12-01, 2022-12-30',
                 '2023-01-01, 2023-01-30', '2023-02-01, 2023-02-25', '2023-03-01, 2023-03-30', '2023-04-01, 2023-04-30']

        for date in dates:
            os.makedirs(output, exist_ok=True)

            data = {
                "client_id": "cdse-public",
                "username": 'copernicus.sd@gmail.com',
                "password": '!!!12345Copernicus',
                "grant_type": "password",
            }
            # data = {
            #     "client_id": "cdse-public",
            #     "username": SCI_HUB_USERNAME_V2,
            #     "password": SCI_HUB_PASSWORD_V2,
            #     "grant_type": "password",
            # }
            try:
                response_token = requests.post(
                    "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
                    data=data,
                    proxies=proxies)
                response_token.raise_for_status()
                print(response_token.json())
            except Exception as e:
                raise Exception(f"Keycloak token creation failed. Reponse from the server was: {response_token.json()}")

            # url_token = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'
            # headers = {
            #     'Content-Type': 'application/x-www-form-urlencoded'
            # }
            # # data = {
            # #     'grant_type': 'client_credentials',
            # #     'client_id': 'sh-ac5e685e-4abe-4e54-bbeb-d52a9d8220dc',
            # #     'client_secret': '8H7N5upOvfBGnJf2tswJvzraDdyDUdQE'
            # # }
            #
            # data = {
            #     'grant_type': 'client_credentials',
            #     'client_id': 'sh-65d404cf-7548-4645-83fc-d3f5d90c0a51',
            #     'client_secret': 'tdXMxSKGc8q1RfkTDZB7pjlwqfFpKsmB'
            # }

            # response_token = requests.post(url_token, headers=headers, data=data)

            url = 'https://catalogue.dataspace.copernicus.eu/odata/v1/Products'
            params = {
                '$filter': f"""OData.CSC.Intersects(area=geography'SRID=4326;{footprint.polygon.wkt}')
                            and ContentDate/Start gt {date[:10]}T00:00:00.000Z and
                            ContentDate/Start lt {date[12:]}T00:00:00.000Z and
                            Collection/Name eq 'SENTINEL-2' and
                            Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and
                            att/OData.CSC.DoubleAttribute/Value lt 25.00) and contains(Name,'S2A_MSIL2A')""",
                '$orderby': 'ContentDate/Start'
            }

            products = requests.get(url, params=params, proxies=proxies).json()['value']
            print(requests.get(url, params=params, proxies=proxies).url)
            print(len(products))
            if len(products) > 1:
                # Получаем координаты TIFF-файла
                tiff_coords = []
                for product in products:
                    check_online_true = product['Online']
                    check_len_coordinates_polygon = len(product['Footprint'].strip("POLYGON((").strip("))").split(","))
                    check_len_coordinates_multipolygon = len(
                        product['Footprint'].strip("MULTIPOLYGON(((").strip(")))").split(","))
                    if check_online_true and check_len_coordinates_polygon == 5:
                        tiff_coords.append(product['Footprint'].strip("geography'"))
                        print(date[:10], date[12:])
                        headers = {'Authorization': f'Bearer {response_token.json()["access_token"]}'}
                        response_download = requests.get(f"{url}({product['Id']})/$value", headers=headers, proxies=proxies)
                        print(response_download.status_code)
                        if response_download.status_code == 200:
                            with open(f"{output}{product['Name']}.zip", 'wb') as f:
                                f.write(response_download.content)
                            print('File saved successfully.')
                            break
                        else:
                            SciHubImageDate.objects.create(area_interest_id=footprint.pk, no_image=True,
                                                           polygon=product['Footprint'].strip("geography'"),
                                                           note=f'Не ---------- ({date})')

                    if check_online_true and check_len_coordinates_multipolygon == 5:
                        tiff_coords.append(product['Footprint'].strip("geography'"))
                        print(date[:10], date[12:])
                        headers = {'Authorization': f'Bearer {response_token.json()["access_token"]}'}
                        response_download = requests.get(f"{url}({product['Id']})/$value", headers=headers, proxies=proxies)
                        print(response_download.status_code, '=================')
                        if response_download.status_code == 200:
                            with open(f"{output}{product['Name']}.zip", 'wb') as f:
                                f.write(response_download.content)
                            print('File saved successfully.')
                            break
                        else:
                            SciHubImageDate.objects.create(area_interest_id=footprint.pk, no_image=True,
                                                           polygon=product['Footprint'].strip("geography'"),
                                                           note=f'Не ---------- ({date})')

                    else:
                        print(date[:10], date[12:], '-------------------', footprint.pk)
                        SciHubImageDate.objects.create(area_interest_id=footprint.pk, no_image=True,
                                                       polygon=product['Footprint'].strip("geography'"),
                                                       note=f'Не удалось получить ни один продукт ({date})')
                        break
            elif len(products) == 0:
                print(date[:10], date[12:], '------------------- elif', footprint.pk)
                SciHubImageDate.objects.create(area_interest_id=footprint.pk, no_image=True,
                                               note=f'Не удалось получить ни один продукт ({date})')

            # Разархивируем файлы
            time.sleep(10)
            for file in os.listdir(output):
                print('ZIP')
                if file.endswith('.zip'):
                    zip_path = os.path.join(output, file)
                    with ZipFile(zip_path) as zipObj:
                        try:
                            zipObj.extractall(output)
                        except zipfile.BadZipFile:
                            shutil.rmtree(output)
                            SciHubImageDate.objects.create(area_interest_id=footprint.pk, no_image=True,
                                                           note=f'Поврежденный файл - ({date})')
                            continue

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
                        for file in os.listdir(os.path.join(output, folder)):
                            if file.endswith(".jpg"):
                                with open(os.path.join(output, folder, file), 'rb') as f:
                                    sci_hub_image_date.image_png.save(f'{file}', f, save=True)
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
                                        sci_hub_image_date.TCI.save(f'TCI_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*B03.*.tif", filename):
                                        sci_hub_image_date.B03.save(f'B03_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*B04.*.tif", filename):
                                        sci_hub_image_date.B04.save(f'B04_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))

                                    elif re.search(".*B08.*.tif", filename):
                                        sci_hub_image_date.B08.save(f'B08_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    sci_hub_image_date.save()
                time.sleep(15)
                shutil.rmtree(output)
            except Exception as e:
                print(e)
    return Response('OK')


"""
retries = 0
                        while retries < 3:  # Максимальное количество повторных попыток
                            try:
                                response_download = requests.get(f"{url}({product['Id']})/$value", headers=headers)
                                response_download.raise_for_status()
                                with open(f"{output}{product['Name']}.zip", 'wb') as f:
                                    f.write(response_download.content)
                                break
                            except requests.exceptions.RequestException as e:
                                print(f"Ошибка при скачивании файла: {str(e)}")
                                print("Повторная попытка скачивания...")
                                retries += 1
                                time.sleep(5)  # Пауза перед повторной попыткой

                        if retries == 3:
                            print(f"Не удалось скачать файл {product['Name']} после 3 попыток")

                        break
"""


class DownloadSatelliteImagesV2(APIView):

    def get(self, request):
        thread_object = Thread(target=download)
        thread_object.start()
        return Response('OK')
        # SCI_HUB_USERNAME_V2 = config('SCI_HUB_USERNAME_V2')
        # SCI_HUB_PASSWORD_V2 = config('SCI_HUB_PASSWORD_V2')
        #
        # # Устанавливаем путь к папке output
        # output = 'output_api/'
        #
        # footprints = [sci_hub_area_interest for sci_hub_area_interest in
        #               SciHubAreaInterest.objects.all().order_by('id')]
        # try:
        #     start_date = request.GET.get('start_date')
        #     end_date = request.GET.get('end_date')
        #     pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        #     if pattern.match(start_date) and pattern.match(end_date):
        #         for footprint in footprints:
        #             os.makedirs(output, exist_ok=True)
        #
        #             data = {
        #                 "client_id": "cdse-public",
        #                 "username": SCI_HUB_USERNAME_V2,
        #                 "password": SCI_HUB_PASSWORD_V2,
        #                 "grant_type": "password",
        #             }
        #             try:
        #                 response_token = requests.post(
        #                     "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
        #                     data=data)
        #                 response_token.raise_for_status()
        #             except Exception as e:
        #                 raise Exception(
        #                     f"Keycloak token creation failed. Reponse from the server was: {response_token.json()}"
        #                 )
        #
        #             url = 'https://catalogue.dataspace.copernicus.eu/odata/v1/Products'
        #             params = {
        #                 '$filter': f"""OData.CSC.Intersects(area=geography'SRID=4326;{footprint.polygon.wkt}')
        #                             and ContentDate/Start gt {start_date}T00:00:00.000Z and
        #                             ContentDate/Start lt {end_date}T00:00:00.000Z and
        #                             Collection/Name eq 'SENTINEL-2' and
        #                             Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and
        #                             att/OData.CSC.DoubleAttribute/Value lt 20.00) and contains(Name,'S2A_MSIL2A')""",
        #                 '$orderby': 'ContentDate/Start'
        #             }
        #
        #             products = requests.get(url, params=params).json()['value']
        #             print(len(products))
        #             if len(products) >= 1:
        #                 # Получаем координаты TIFF-файла
        #                 tiff_coords = []
        #                 for product in products:
        #                     check_online_true = product['Online']
        #                     check_len_coordinates = len(product['Footprint'].strip("POLYGON((").strip("))").split(","))
        #                     if check_online_true and check_len_coordinates == 5:
        #                         tiff_coords.append(product['Footprint'].strip("geography'"))
        #                         headers = {'Authorization': f'Bearer {response_token.json()["access_token"]}'}
        #                         response_download = requests.get(f"{url}({product['Id']})/$value", headers=headers)
        #                         with open(f"{output}{product['Name']}.zip", 'wb') as f:
        #                             f.write(response_download.content)
        #                         break
        #                     elif not check_online_true and check_len_coordinates != 5:
        #                         print('==========')
        #                         return JsonResponse(
        #                             {'message': f'Не удалось получить одиного космоснимка за этот период '
        #                                         f'({start_date}/{end_date}) '}, status=400)
        #             elif len(products) == 0:
        #                 return JsonResponse({'message': f'Не удалось получить ни одиного космоснимка за этот период '
        #                                                 f'({start_date} / {end_date}) '}, status=400)
        #             # Разархивируем файлы
        #             time.sleep(10)
        #             for file in os.listdir(output):
        #                 print('ZIP')
        #                 if file.endswith('.zip'):
        #                     with ZipFile(f"{output}{file}") as zipObj:
        #                         zipObj.extractall(output)
        #
        #             # Конвертируем jp2 в tiff и сохраняем в базу данных
        #             time.sleep(20)
        #             try:
        #                 for folder in os.listdir(output):
        #                     if folder.endswith('.SAFE'):
        #                         for file in os.listdir(os.path.join(output, folder, 'GRANULE')):
        #                             if file.startswith('L2A_'):
        #                                 img_data_path = os.path.join(output, folder, 'GRANULE', file, 'IMG_DATA',
        #                                                              'R10m')
        #                                 for filename in os.listdir(img_data_path):
        #                                     if re.search(".*B.*", filename):
        #                                         jp2_path = os.path.join(img_data_path, filename)
        #                                         tiff_path = os.path.join(img_data_path, filename[:-3] + 'tif')
        #                                         gdal.Translate(tiff_path, jp2_path, format='GTiff')
        #                                     elif re.search(".*TCI.*", filename):
        #                                         jp2_path = os.path.join(img_data_path, filename)
        #                                         tiff_path = os.path.join(img_data_path, filename[:-3] + 'tif')
        #                                         gdal.Translate(tiff_path, jp2_path, format='GTiff')
        #
        #                     # Tiff сохраняем в базу данных
        #                     if folder.endswith('.SAFE'):
        #                         img_date = datetime.strptime(os.path.basename(folder)[11:19], '%Y%m%d')
        #                         sci_hub_image_date = SciHubImageDate(date=img_date, area_interest_id=footprint.pk)
        #                         sci_hub_image_date.name_product = folder
        #                         for file in os.listdir(os.path.join(output, folder)):
        #                             if file.endswith(".jpg"):
        #                                 with open(os.path.join(output, folder, file), 'rb') as f:
        #                                     sci_hub_image_date.image_png.save(f'{file}', f, save=True)
        #                         for file in os.listdir(os.path.join(output, folder, 'GRANULE')):
        #                             if file.startswith('L2A_'):
        #                                 img_data_path = os.path.join(output, folder, 'GRANULE', file, 'IMG_DATA',
        #                                                              'R10m')
        #                                 for filename in os.listdir(img_data_path):
        #                                     if re.search(".*B02.*.tif", filename):
        #                                         # Создаем экземпляр модели изображения
        #                                         sci_hub_image_date.polygon = tiff_coords[0]
        #                                         sci_hub_image_date.B02.save(f'B02_area_interest_id-{footprint.pk}.tif',
        #                                                                     open(f"{img_data_path}/{filename}", 'rb'))
        #                                     elif re.search(".*TCI.*.tif", filename):
        #                                         sci_hub_image_date.TCI.save(f'TCI_area_interest_id-{footprint.pk}.tif',
        #                                                                     open(f"{img_data_path}/{filename}", 'rb'))
        #                                     elif re.search(".*B03.*.tif", filename):
        #                                         sci_hub_image_date.B03.save(f'B03_area_interest_id-{footprint.pk}.tif',
        #                                                                     open(f"{img_data_path}/{filename}", 'rb'))
        #                                     elif re.search(".*B04.*.tif", filename):
        #                                         sci_hub_image_date.B04.save(f'B04_area_interest_id-{footprint.pk}.tif',
        #                                                                     open(f"{img_data_path}/{filename}", 'rb'))
        #
        #                                     elif re.search(".*B08.*.tif", filename):
        #                                         sci_hub_image_date.B8A.save(f'B08_area_interest_id-{footprint.pk}.tif',
        #                                                                     open(f"{img_data_path}/{filename}", 'rb'))
        #                                     sci_hub_image_date.save()
        #                 time.sleep(15)
        #                 shutil.rmtree(output)
        #             except Exception as e:
        #                 print(e)
        #         return JsonResponse({'message': 'OK'})
        #     else:
        #         return JsonResponse({'message': 'Неверный формат даты, должен содержать формат (Y-M-D)'}, status=400)
        # except Exception as e:
        #     return Response(data={"message": "parameter 'start_date and end_date' is required"}, status=400)


"""
https://catalogue.dataspace.copernicus.eu/odata/v1/Products?%24filter=OData.CSC.Intersects%28area%3Dgeography%27SRID%3D4326%3BPOLYGON+%28%2877.752132+41.660601%2C+77.752132+41.789745%2C+77.993832+41.789745%2C+77.993832+41.660601%2C+77.752132+41.660601%29%29%27%29%0A++++++++++++++++++++++++++++and+ContentDate%2FStart+gt+2020-01-01T00%3A00%3A00.000Z+and%0A++++++++++++++++++++++++++++ContentDate%2FStart+lt+2020-01-30T00%3A00%3A00.000Z+and%0A++++++++++++++++++++++++++++Collection%2FName+eq+%27SENTINEL-2%27+and%0A++++++++++++++++++++++++++++Attributes%2FOData.CSC.DoubleAttribute%2Fany%28att%3Aatt%2FName+eq+%27cloudCover%27+and%0A++++++++++++++++++++++++++++att%2FOData.CSC.DoubleAttribute%2FValue+lt+25.00%29+and+contains%28Name%2C%27S2A_MSIL2A%27%29&%24orderby=ContentDate%2FStart

"""
