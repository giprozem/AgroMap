import os
import re
import shutil
import time
from datetime import datetime
from rest_framework.response import Response
from sentinelsat import SentinelAPI
from zipfile import ZipFile
from osgeo import gdal
from datetime import date

from indexes.models import SciHubImageDate, SciHubAreaInterest
from decouple import config

SCI_HUB_USERNAME = config('SCI_HUB_USERNAME')
SCI_HUB_PASSWORD = config('SCI_HUB_PASSWORD')


def run():
    # Set the path to the output folder
    output = 'output/'

    # Download images using the SentinelAPI with Sci-hub credentials
    api = SentinelAPI(SCI_HUB_USERNAME, SCI_HUB_PASSWORD, 'https://scihub.copernicus.eu/dhus')

    current_date = date.today()
    first_day_of_previous_month = date(current_date.year, current_date.month - 1, 1)

    # Get a list of areas of interest
    footprints = [sci_hub_area_interest for sci_hub_area_interest in SciHubAreaInterest.objects.all().order_by('id')]

    # Iterate through areas of interest
    for footprint in footprints:
        # Create output directory if it does not exist
        os.makedirs(output, exist_ok=True)

        # Fetch the products from API using given date, platform, processing level, and cloud coverage parameters
        products = api.query(footprint.polygon.wkt,
                             date=(first_day_of_previous_month.strftime("%Y%m%d"), current_date.strftime("%Y%m%d")),
                             platformname='Sentinel-2',
                             processinglevel='Level-1C',
                             cloudcoverpercentage=(0, 20))

        # Check if there are products available
        if len(products) > 1:
            # Extract the coordinates of the TIFF files
            tiff_coords = []
            for i in products:
                metadata_product = api.get_product_odata(i)
                check_len_coordinates = len(metadata_product['footprint'].strip("POLYGON((").strip("))").split(","))
                if check_len_coordinates == 5:
                    tiff_coords.append(metadata_product['footprint'])
                    # Download the product and save it to the output directory
                    api.download(products[i]['uuid'], directory_path=output)
                    break
        else:
            # If no products found, create an entry in the database with a note
            SciHubImageDate.objects.create(area_interest_id=footprint.pk, no_image=True,
                                           note=f'No products found between '
                                                f'{first_day_of_previous_month.strftime("%Y.%m.%d")} and '
                                                f'{current_date.strftime("%Y.%m.%d")}')
            continue

        # Extract the files after a delay
        time.sleep(10)
        for file in os.listdir(output):
            if file.endswith('.zip'):
                with ZipFile(f"{output}{file}") as zipObj:
                    zipObj.extractall(output)

        # Convert jp2 images to tiff format and save in the database
        time.sleep(20)
        try:
            for folder in os.listdir(output):
                if folder.endswith('.SAFE'):
                    for file in os.listdir(os.path.join(output, folder, 'GRANULE')):
                        if file.startswith('L1C_'):
                            img_data_path = os.path.join(output, folder, 'GRANULE', file, 'IMG_DATA')
                            # Convert each jp2 file to tiff using gdal and save in the database
                            for filename in os.listdir(img_data_path):
                                if re.search(".*B.*", filename) or re.search(".*TCI.*", filename):
                                    jp2_path = os.path.join(img_data_path, filename)
                                    tiff_path = os.path.join(img_data_path, filename[:-3] + 'tif')
                                    gdal.Translate(tiff_path, jp2_path, format='GTiff')

                # Save TIFF files in the database
                if folder.endswith('.SAFE'):
                    img_date = datetime.strptime(os.path.basename(folder)[11:19], '%Y%m%d')
                    sci_hub_image_date = SciHubImageDate(date=img_date, area_interest_id=footprint.pk)
                    sci_hub_image_date.name_product = folder
                    # For each image in the folder, create a SciHubImageDate object and save the image and its details in the database
                    for file in os.listdir(os.path.join(output, folder)):
                        if file.endswith(".jpg"):
                            with open(os.path.join(output, folder, file), 'rb') as f:
                                sci_hub_image_date.image_png.save(f'{file}', f, save=True)
                    for file in os.listdir(os.path.join(output, folder, 'GRANULE')):
                        if file.startswith('L1C_'):
                            img_data_path = os.path.join(output, folder, 'GRANULE', file, 'IMG_DATA')
                            for filename in os.listdir(img_data_path):
                                if re.search(".*B01.*.tif", filename):
                                    sci_hub_image_date.B01.save(f'B01_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B02.*.tif", filename):
                                    sci_hub_image_date.polygon = tiff_coords[0]
                                    sci_hub_image_date.B02.save(f'B02_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B03.*.tif", filename):
                                    sci_hub_image_date.B03.save(f'B03_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B04.*.tif", filename):
                                    sci_hub_image_date.B04.save(f'B04_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B05.*.tif", filename):
                                    sci_hub_image_date.B05.save(f'B05_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B06.*.tif", filename):
                                    sci_hub_image_date.B06.save(f'B06_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B07.*.tif", filename):
                                    sci_hub_image_date.B07.save(f'B07_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B08.*.tif", filename):
                                    sci_hub_image_date.B08.save(f'B08_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B8A.*.tif", filename):
                                    sci_hub_image_date.B8A.save(f'B8A_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B09.*.tif", filename):
                                    sci_hub_image_date.B09.save(f'B09_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B10.*.tif", filename):
                                    sci_hub_image_date.B10.save(f'B10_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B11.*.tif", filename):
                                    sci_hub_image_date.B11.save(f'B11_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*B12.*.tif", filename):
                                    sci_hub_image_date.B12.save(f'B12_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                elif re.search(".*TCI.*.tif", filename):
                                    sci_hub_image_date.TCI.save(f'TCI_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                                open(f"{img_data_path}/{filename}", 'rb'))
                                sci_hub_image_date.save()
            # Clean up the output directory
            time.sleep(15)
            shutil.rmtree(output)
        except Exception as e:
            print(e)
    return Response('OK')
