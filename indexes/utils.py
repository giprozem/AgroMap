import glob
import io
import os
import re
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from zipfile import ZipFile

import matplotlib.pyplot as plt
import rasterio
import requests
from PIL import Image
from decouple import config
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from osgeo import gdal
from rest_framework.response import Response

from culture_model.models import VegetationIndex
from gip.models import Contour
from indexes.index_funcs import cutting_tiff
from indexes.index_funcs.ndmi_funcs import average_ndmi, ndmi_calculator
from indexes.index_funcs.ndre_funcs import average_ndre, ndre_calculator
from indexes.index_funcs.ndvi_funcs import average_ndvi, ndvi_calculator
from indexes.index_funcs.ndwi_funcs import average_ndwi, ndwi_calculator
from indexes.index_funcs.savi_funcs import average_savi, savi_calculator
from indexes.index_funcs.vari_funcs import average_vari, vari_calculator
from indexes.models import ActualVegIndex, IndexCreatingReport, IndexMeaning, SciHubAreaInterest
from indexes.models import SciHubImageDate


def veg_index_creating(image_date):
    try:
        contours = Contour.objects.filter(polygon__coveredby=image_date.polygon)
        for contour in contours:
            polygon = GEOSGeometry(contour.polygon).geojson
            file_name = f'temporary file {datetime.now()}'
            output_path_b02 = f"./media/B02_{file_name}.tiff"
            output_path_b03 = f"./media/B03_{file_name}.tiff"
            output_path_b04 = f"./media/B04_{file_name}.tiff"
            output_path_b07 = f"./media/B07_{file_name}.tiff"
            output_path_b8a = f"./media/B8A_{file_name}.tiff"
            output_path_b11 = f"./media/B11_{file_name}.tiff"

            input_path_b02 = f'./media/{image_date.B02}'
            input_path_b03 = f'./media/{image_date.B03}'
            input_path_b04 = f'./media/{image_date.B04}'
            input_path_b07 = f'./media/{image_date.B07}'
            input_path_b8a = f'./media/{image_date.B8A}'
            input_path_b11 = f'./media/{image_date.B11}'
            gdal.UseExceptions()
            cutting_error = []

            try:
                cutting_tiff(outputpath=output_path_b02, inputpath=input_path_b02, polygon=polygon)
            except Exception as b02_error:
                cutting_error.append(f'B02 layer cutting error {b02_error}, ')
            try:
                cutting_tiff(outputpath=output_path_b03, inputpath=input_path_b03, polygon=polygon)
            except Exception as b03_error:
                cutting_error.append(f'B03 layer cutting error cutting error {b03_error}, ')
            try:
                cutting_tiff(outputpath=output_path_b04, inputpath=input_path_b04, polygon=polygon)
            except Exception as b04_error:
                cutting_error.append(f'B04 layer cutting error {b04_error}, ')
            try:
                cutting_tiff(outputpath=output_path_b07, inputpath=input_path_b07, polygon=polygon)
            except Exception as b07_error:
                cutting_error.append(f'B07 layer cutting error {b07_error}, ')
            try:
                cutting_tiff(outputpath=output_path_b8a, inputpath=input_path_b8a, polygon=polygon)
            except Exception as b8a_error:
                cutting_error.append(f'B8A layer cutting error {b8a_error}, ')
            try:
                cutting_tiff(outputpath=output_path_b11, inputpath=input_path_b11, polygon=polygon)
            except Exception as b11_error:
                cutting_error.append(f'B11 layer cutting error {b11_error}')

            for veg_index in VegetationIndex.objects.all():
                if IndexCreatingReport.objects.filter(veg_index=veg_index, contour=contour, satellite_image=image_date):
                    pass
                else:
                    if IndexCreatingReport.objects.filter(
                            contour_id=contour.id,
                            is_processed=True,
                            satellite_image=image_date,
                            veg_index=veg_index
                    ):
                        pass
                    else:
                        try:
                            if veg_index.name == 'NDVI':
                                average_value = average_ndvi(red_file=output_path_b04, nir_file=output_path_b8a)

                                result_to_save = ndvi_calculator(
                                    B04=output_path_b04,
                                    B08=output_path_b8a,
                                    saving_file_name=file_name
                                )

                            elif veg_index.name == 'NDMI':
                                average_value = average_ndmi(swir_file=output_path_b11, nir_file=output_path_b8a)

                                result_to_save = ndmi_calculator(
                                    B11=output_path_b11,
                                    B08=output_path_b8a,
                                    saving_file_name=file_name
                                )

                            elif veg_index.name == 'NDWI':
                                average_value = average_ndwi(green_file=output_path_b03, nir_file=output_path_b8a)

                                result_to_save = ndwi_calculator(
                                    B03=output_path_b03,
                                    B08=output_path_b8a,
                                    saving_file_name=file_name
                                )
                            elif veg_index.name == 'NDRE':
                                average_value = average_ndre(red_file=output_path_b07, nir_file=output_path_b8a)

                                result_to_save = ndre_calculator(
                                    B07=output_path_b07,
                                    B8A=output_path_b8a,
                                    saving_file_name=file_name
                                )
                            elif veg_index.name == 'SAVI':
                                average_value = average_savi(red_file=output_path_b04, nir_file=output_path_b8a)

                                result_to_save = savi_calculator(
                                    B04=output_path_b04,
                                    B08=output_path_b8a,
                                    saving_file_name=file_name
                                )

                            elif veg_index.name == 'VARI':
                                average_value = average_vari(
                                    red_file=output_path_b04,
                                    green_file=output_path_b03,
                                    blue_file=output_path_b02
                                )

                                result_to_save = vari_calculator(
                                    B02=output_path_b02,
                                    B03=output_path_b03,
                                    B04=output_path_b04,
                                    saving_file_name=file_name
                                )

                            else:
                                raise ObjectDoesNotExist(
                                    _('Ошибка создания индекса растительности, проверьте имена индексов'))
                            meaning_of_average_value = IndexMeaning.objects.filter(
                                index=veg_index
                            ).filter(
                                min_index_value__lt=average_value
                            ).filter(
                                max_index_value__gte=average_value
                            ).first()

                            actual = ActualVegIndex.objects.create(
                                average_value=average_value,
                                meaning_of_average_value=meaning_of_average_value,
                                contour_id=contour.id,
                                index_id=veg_index.id,
                                date=image_date.date
                            )
                            actual.index_image.save(f'{file_name}.png', result_to_save)

                            IndexCreatingReport.objects.create(
                                contour_id=contour.id,
                                veg_index_id=veg_index.id,
                                satellite_image_id=image_date.id,
                                is_processed=True,
                                process_error='No error'
                            )
                        except Exception as e:
                            plt.close()
                            # creating report
                            IndexCreatingReport.objects.create(
                                contour_id=contour.id,
                                veg_index_id=veg_index.id,
                                satellite_image_id=image_date.id,
                                is_processed=False,
                                process_error=f'{e}, {cutting_error}'
                            )

                        # Search files with .tiff extension in current directory
                    pattern = "./media/*.tiff"
                    files = glob.glob(pattern)

                    # deleting the files with tiff extension
                    for file in files:
                        os.remove(file)

    except Exception as e:
        print(e)
        IndexCreatingReport.objects.create(
            contour_id=None,
            veg_index_id=None,
            satellite_image_id=image_date.id,
            is_processed=False,
            process_error=f'Have no contours in this satellite image. Error is - {e}'
        )
        pass


def create_veg_indexes():
    image_dates = SciHubImageDate.objects.all()

    with ThreadPoolExecutor(max_workers=40) as executor:
        executor.map(veg_index_creating, image_dates)


def creating_veg_index_to_given_image(satellite_image):
    contours = Contour.objects.filter(polygon__coveredby=satellite_image.polygon)

    for contour in contours:
        polygon = GEOSGeometry(contour.polygon).geojson
        file_name = f'temporary file {datetime.now()}'
        output_path_b02 = f"./media/B02_{file_name}.tiff"
        output_path_b03 = f"./media/B03_{file_name}.tiff"
        output_path_b04 = f"./media/B04_{file_name}.tiff"
        output_path_b07 = f"./media/B07_{file_name}.tiff"
        output_path_b8a = f"./media/B8A_{file_name}.tiff"
        output_path_b11 = f"./media/B11_{file_name}.tiff"

        input_path_b02 = f'./media/{satellite_image.B02}'
        input_path_b03 = f'./media/{satellite_image.B03}'
        input_path_b04 = f'./media/{satellite_image.B04}'
        input_path_b07 = f'./media/{satellite_image.B07}'
        input_path_b8a = f'./media/{satellite_image.B8A}'
        input_path_b11 = f'./media/{satellite_image.B11}'
        gdal.UseExceptions()
        cutting_error = []

        try:
            cutting_tiff(outputpath=output_path_b02, inputpath=input_path_b02, polygon=polygon)
        except Exception as b02_error:
            cutting_error.append(f'B02 layer cutting error {b02_error}, ')
        try:
            cutting_tiff(outputpath=output_path_b03, inputpath=input_path_b03, polygon=polygon)
        except Exception as b03_error:
            cutting_error.append(f'B03 layer cutting error cutting error {b03_error}, ')
        try:
            cutting_tiff(outputpath=output_path_b04, inputpath=input_path_b04, polygon=polygon)
        except Exception as b04_error:
            cutting_error.append(f'B04 layer cutting error {b04_error}, ')
        try:
            cutting_tiff(outputpath=output_path_b07, inputpath=input_path_b07, polygon=polygon)
        except Exception as b07_error:
            cutting_error.append(f'B07 layer cutting error {b07_error}, ')
        try:
            cutting_tiff(outputpath=output_path_b8a, inputpath=input_path_b8a, polygon=polygon)
        except Exception as b8a_error:
            cutting_error.append(f'B8A layer cutting error {b8a_error}, ')
        try:
            cutting_tiff(outputpath=output_path_b11, inputpath=input_path_b11, polygon=polygon)
        except Exception as b11_error:
            cutting_error.append(f'B11 layer cutting error {b11_error}')

        for veg_index in VegetationIndex.objects.all():
            if IndexCreatingReport.objects.filter(veg_index=veg_index, contour=contour,
                                                  satellite_image=satellite_image):
                pass
            else:
                if IndexCreatingReport.objects.filter(
                        contour_id=contour.id,
                        is_processed=True,
                        satellite_image=satellite_image,
                        veg_index=veg_index
                ):

                    pass
                else:
                    try:
                        if veg_index.name == 'NDVI':
                            average_value = average_ndvi(red_file=output_path_b04, nir_file=output_path_b8a)

                            result_to_save = ndvi_calculator(
                                B04=output_path_b04,
                                B08=output_path_b8a,
                                saving_file_name=file_name
                            )

                        elif veg_index.name == 'NDMI':
                            average_value = average_ndmi(swir_file=output_path_b11, nir_file=output_path_b8a)

                            result_to_save = ndmi_calculator(
                                B11=output_path_b11,
                                B08=output_path_b8a,
                                saving_file_name=file_name
                            )

                        elif veg_index.name == 'NDWI':
                            average_value = average_ndwi(green_file=output_path_b03, nir_file=output_path_b8a)

                            result_to_save = ndwi_calculator(
                                B03=output_path_b03,
                                B08=output_path_b8a,
                                saving_file_name=file_name
                            )
                        elif veg_index.name == 'NDRE':
                            average_value = average_ndre(red_file=output_path_b07, nir_file=output_path_b8a)

                            result_to_save = ndre_calculator(
                                B07=output_path_b07,
                                B8A=output_path_b8a,
                                saving_file_name=file_name
                            )
                        elif veg_index.name == 'SAVI':
                            average_value = average_savi(red_file=output_path_b04, nir_file=output_path_b8a)

                            result_to_save = savi_calculator(
                                B04=output_path_b04,
                                B08=output_path_b8a,
                                saving_file_name=file_name
                            )

                        elif veg_index.name == 'VARI':
                            average_value = average_vari(
                                red_file=output_path_b04,
                                green_file=output_path_b03,
                                blue_file=output_path_b02
                            )

                            result_to_save = vari_calculator(
                                B02=output_path_b02,
                                B03=output_path_b03,
                                B04=output_path_b04,
                                saving_file_name=file_name
                            )

                        else:
                            raise ObjectDoesNotExist(
                                _('Ошибка создания индекса растительности, проверьте имена индексов'))
                        meaning_of_average_value = IndexMeaning.objects.filter(
                            index=veg_index
                        ).filter(
                            min_index_value__lt=average_value
                        ).filter(
                            max_index_value__gte=average_value
                        ).first()

                        actual = ActualVegIndex.objects.create(
                            average_value=average_value,
                            meaning_of_average_value=meaning_of_average_value,
                            contour_id=contour.id,
                            index_id=veg_index.id,
                            date=satellite_image.date
                        )
                        actual.index_image.save(f'{file_name}.png', result_to_save)

                        IndexCreatingReport.objects.create(
                            contour_id=contour.id,
                            veg_index_id=veg_index.id,
                            satellite_image_id=satellite_image.id,
                            is_processed=True,
                            process_error='No error'
                        )
                    except Exception as e:
                        plt.close()
                        # creating report
                        IndexCreatingReport.objects.create(
                            contour_id=contour.id,
                            veg_index_id=veg_index.id,
                            satellite_image_id=satellite_image.id,
                            is_processed=False,
                            process_error=f'{e}, {cutting_error}'
                        )

        # Search files with .tiff extension in current directory
        pattern = "./media/*.tiff"
        files = glob.glob(pattern)

        # deleting the files with tiff extension
        for file in files:
            os.remove(file)


def download_satellite_images_v2():
    SCI_HUB_USERNAME_V2 = config('SCI_HUB_USERNAME_V2')
    SCI_HUB_PASSWORD_V2 = config('SCI_HUB_PASSWORD_V2')

    # Устанавливаем путь к папке output
    output = 'output/'

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
                                img_data_path = os.path.join(output, folder, 'GRANULE', file, 'IMG_DATA', 'R20m')
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
                                                             'R20m')
                                for filename in os.listdir(img_data_path):
                                    if re.search(".*B01.*.tif", filename):
                                        sci_hub_image_date.B01.save(f'B01_area_interest_id-{footprint.pk}.tif',

                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*B02.*.tif", filename):
                                        # Создаем экземпляр модели изображения
                                        sci_hub_image_date.polygon = tiff_coords[0]
                                        sci_hub_image_date.B02.save(f'B02_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*TCI.*.tif", filename):
                                        print('TCI--------------------')
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
                                    elif re.search(".*B05.*.tif", filename):
                                        sci_hub_image_date.B05.save(f'B05_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*B06.*.tif", filename):
                                        sci_hub_image_date.B06.save(f'B06_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*B07.*.tif", filename):
                                        sci_hub_image_date.B07.save(f'B07_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*B08.*.tif", filename):
                                        sci_hub_image_date.B08.save(f'B08_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*B8A.*.tif", filename):
                                        sci_hub_image_date.B8A.save(f'B8A_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*B09.*.tif", filename):
                                        sci_hub_image_date.B09.save(f'B09_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*B10.*.tif", filename):
                                        sci_hub_image_date.B10.save(f'B10_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*B11.*.tif", filename):
                                        sci_hub_image_date.B11.save(f'B11_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    elif re.search(".*B12.*.tif", filename):
                                        sci_hub_image_date.B12.save(f'B12_area_interest_id-{footprint.pk}.tif',
                                                                    open(f"{img_data_path}/{filename}", 'rb'))
                                    sci_hub_image_date.save()
                time.sleep(15)
                shutil.rmtree(output)
            except Exception as e:
                print(e)
    return Response('OK')
