import os
import re
import shutil
import time
from zipfile import ZipFile
from datetime import datetime
from decouple import config
from osgeo import gdal
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from sentinel2_downloader import SentinelAPI

from indexes.models import SciHubAreaInterest
from indexes.models import SciHubImageDate


class DownloadSatelliteImagesV2(APIView):
    permission_classes = [IsAdminUser, ]
    """
    A class used to download satellite images through the Sentinel API.
    """

    def get(self, request):
        """
        The 'get' function is called when an HTTP GET request is made to the endpoint associated with this view.
        It retrieves and downloads satellite images based on provided date range and footprint_id.
        """

        # Obtain start_date, end_date, and footprint_id from the request
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        footprint_id = request.GET.get('footprint_id')

        # Credentials for the Sentinel API
        SCI_HUB_USERNAME_V2 = config('SCI_HUB_USERNAME_V2')
        SCI_HUB_PASSWORD_V2 = config('SCI_HUB_PASSWORD_V2')

        # Initialize Sentinel API
        api = SentinelAPI(username=SCI_HUB_USERNAME_V2, password=SCI_HUB_PASSWORD_V2)

        # Set path to the output folder
        output = 'output_satellite_images_script/'

        # If start_date, end_date and footprint_id are provided
        if footprint_id and start_date and end_date:
            print(footprint_id)
            print(start_date)
            print(end_date)
            # Convert footprint_id from comma-separated string to list of integers
            footprint_id = list(map(int, footprint_id.split(',')))
            # Fetch the area of interest records corresponding to the provided footprint_ids
            footprints = [sci_hub_area_interest for sci_hub_area_interest in
                          SciHubAreaInterest.objects.filter(id__in=footprint_id).order_by('id')]

            # For each area of interest (footprint)
            for footprint in footprints:
                # Create the output directory if it doesn't exist
                os.makedirs(output, exist_ok=True)
                # Query the Sentinel API for the images
                products = api.query(footprint=footprint.polygon.wkt,
                                     start_date=f'{start_date}', end_date=f'{end_date}', cloud_cover_percentage='20',
                                     product_type='MSIL1C',
                                     platform_name='SENTINEL-2')

                try:
                    if len(products) > 1:
                        tiff_coords = []
                        for product in products:
                            check_len_coordinates = len(product['Footprint'].strip("POLYGON((").strip("))").split(","))
                            if check_len_coordinates == 5:
                                tiff_coords.append(product['Footprint'].strip("geography'"))
                                api.download(product_id=product['Id'], directory_path=output)
                                break
                            else:
                                SciHubImageDate.objects.create(area_interest_id=footprint.pk, no_image=True,
                                                               polygon=product['Footprint'].strip("geography'"),
                                                               note=f'Не удалось получить ни один продукт (2023-05-01/2023-05-30)')
                                break
                    elif len(products) == 0:
                        SciHubImageDate.objects.create(area_interest_id=footprint.pk, no_image=True,
                                                       note=f'Не удалось получить ни один продукт (2023-05-01/2023-05-30)')
                except KeyError:
                    SciHubImageDate.objects.create(area_interest_id=footprint.pk, no_image=True,
                                                   note=f'Не удалось получить ни один продукт (2023-05-01/2023-05-30)')
                    continue

                time.sleep(10)  # Pausing the execution for 10 seconds

                # Looping through all the files in the 'output' directory
                for file in os.listdir(output):
                    print('ZIP')  # Print 'ZIP' for debugging purposes
                    # If the file ends with '.zip'
                    if file.endswith('.zip'):
                        # Open the zip file and extract all files into the 'output' directory
                        with ZipFile(f"{output}{file}") as zipObj:
                            zipObj.extractall(output)

                time.sleep(20)  # Pausing the execution for 20 seconds

                # Handling any possible errors with a try-except block
                try:
                    # Looping through all the folders in the 'output' directory
                    for folder in os.listdir(output):
                        # If the folder ends with '.SAFE'
                        if folder.endswith('.SAFE'):
                            # Looping through all the files in the 'GRANULE' subdirectory of the folder
                            for file in os.listdir(os.path.join(output, folder, 'GRANULE')):
                                # If the file starts with 'L1C_'
                                if file.startswith('L1C_'):
                                    # Define the path to the 'IMG_DATA' subdirectory
                                    img_data_path = os.path.join(output, folder, 'GRANULE', file, 'IMG_DATA')
                                    # Looping through all the filenames in the 'IMG_DATA' directory
                                    for filename in os.listdir(img_data_path):
                                        # If the filename matches the regex pattern ".*B.*"
                                        if re.search(".*B.*", filename):
                                            # Define the path to the jp2 file and the tiff file
                                            jp2_path = os.path.join(img_data_path, filename)
                                            tiff_path = os.path.join(img_data_path, filename[:-3] + 'tif')
                                            # Convert the jp2 file to a tiff file
                                            gdal.Translate(tiff_path, jp2_path, format='GTiff')
                                        # If the filename matches the regex pattern ".*TCI.*"
                                        elif re.search(".*TCI.*", filename):
                                            # Define the path to the jp2 file and the tiff file
                                            jp2_path = os.path.join(img_data_path, filename)
                                            tiff_path = os.path.join(img_data_path, filename[:-3] + 'tif')
                                            # Convert the jp2 file to a tiff file
                                            gdal.Translate(tiff_path, jp2_path, format='GTiff')

                        # Saving the Tiff files to the database
                        # If the folder ends with '.SAFE'
                        if folder.endswith('.SAFE'):
                            # Parse the date from the folder name
                            img_date = datetime.strptime(os.path.basename(folder)[11:19], '%Y%m%d')
                            # Create a new SciHubImageDate object
                            sci_hub_image_date = SciHubImageDate(date=img_date, area_interest_id=footprint.pk)
                            sci_hub_image_date.name_product = folder
                            # Looping through all the files in the folder
                            for file in os.listdir(os.path.join(output, folder)):
                                # If the file ends with ".jpg"
                                if file.endswith(".jpg"):
                                    # Open the jpg file and save it to the 'image_png' field of the SciHubImageDate object
                                    with open(os.path.join(output, folder, file), 'rb') as f:
                                        sci_hub_image_date.image_png.save(f'{file}', f, save=True)
                            # Looping through all the files in the 'GRANULE' subdirectory of the folder
                            for file in os.listdir(os.path.join(output, folder, 'GRANULE')):
                                # If the file starts with 'L1C_'
                                if file.startswith('L1C_'):
                                    # Define the path to the 'IMG_DATA' subdirectory
                                    img_data_path = os.path.join(output, folder, 'GRANULE', file, 'IMG_DATA')
                                    # Looping through all the filenames in the 'IMG_DATA' directory
                                    for filename in os.listdir(img_data_path):
                                        # If the filename matches the regex pattern, save it to the corresponding field of the SciHubImageDate object
                                        # These following lines do the same for different bands and different filename patterns.
                                        # Here the 'open' function is used to read the file in binary mode, and the 'save' method is called to save the file to the database.
                                        if re.search(".*B01.*.tif", filename):
                                            sci_hub_image_date.B01.save(f'B01_area_interest_id-{footprint.pk}.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        elif re.search(".*B02.*.tif", filename):
                                            sci_hub_image_date.polygon = tiff_coords[0]
                                            sci_hub_image_date.B02.save(f'B02_area_interest_id-{footprint.pk}.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
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
                                        elif re.search(".*TCI.*.tif", filename):
                                            sci_hub_image_date.TCI.save(f'TCI_area_interest_id-{footprint.pk}.tif',
                                                                        open(f"{img_data_path}/{filename}", 'rb'))
                                        sci_hub_image_date.save()
                    time.sleep(5)  # Pausing the execution for 5 seconds
                    # Removing the 'output' directory and all its contents
                    shutil.rmtree(output)
                except Exception as e:
                    print(e)
        return Response('OK')
