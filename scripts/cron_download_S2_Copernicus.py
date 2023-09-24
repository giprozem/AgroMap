import os
import re
import shutil
import time
from datetime import datetime, date

from rest_framework import status
from rest_framework.response import Response
from sentinelsat import SentinelAPI
from zipfile import ZipFile
from osgeo import gdal

from indexes.models import SciHubImageDate, SciHubAreaInterest
from decouple import config

# API credentials for Sentinel Hub
SCI_HUB_USERNAME = config('SCI_HUB_USERNAME')
SCI_HUB_PASSWORD = config('SCI_HUB_PASSWORD')


def extract_files(output):
    """Unzip all ZIP files in the specified directory."""
    for file in os.listdir(output):
        if file.endswith('.zip'):
            with ZipFile(os.path.join(output, file)) as zipObj:
                zipObj.extractall(output)


def convert_jp2_to_tif(jp2_path, tif_path):
    """Convert a JP2 file to a TIFF format using GDAL."""
    ds = gdal.Translate(tif_path, jp2_path, format='GTiff')
    del ds


def convert_and_save_files(output, folder, tiff_coords, footprint):
    """Convert JP2 files to TIFF and save satellite image metadata to the SciHubImageDate database model."""
    # Extract the image date from the folder name
    img_date = datetime.strptime(os.path.basename(folder)[11:19], '%Y%m%d')
    sci_hub_image_date = SciHubImageDate(date=img_date, area_interest_id=footprint.pk)
    sci_hub_image_date.name_product = folder  # Set the product name as the folder name

    # Define the list of bands we're interested in
    bands = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B09', 'B10', 'B11', 'B12', 'TCI']

    # Construct the path to the image data
    img_data_path = os.path.join(output, folder, 'GRANULE', next(
        filter(lambda x: x.startswith('L1C_'), os.listdir(os.path.join(output, folder, 'GRANULE')))), 'IMG_DATA')

    # Iterate over files and convert the ones corresponding to the bands
    for filename in os.listdir(img_data_path):
        for band in bands:
            if re.search(f".*{band}.*.jp2", filename):
                jp2_path = os.path.join(img_data_path, filename)
                tif_filename = filename.replace('.jp2', '.tif')
                tif_path = os.path.join(img_data_path, tif_filename)

                # Convert JP2 to TIFF
                convert_jp2_to_tif(jp2_path, tif_path)

                # Save the TIFF image data to the corresponding band in the database
                getattr(sci_hub_image_date, band).save(f'{band}_area_interest_id-{img_date}-{footprint.pk}.tif',
                                                       open(tif_path, 'rb'))

                # If the band is B02, set the polygon for the image date
                if band == 'B02':
                    sci_hub_image_date.polygon = tiff_coords[0]

    # Save the record to the database
    sci_hub_image_date.save()


def run():
    """Fetch, process, and save Sentinel-2 satellite images for all area of interests."""
    output = 'output_satellite_images/'
    os.makedirs(output, exist_ok=True)  # Ensure the output directory exists

    # Initialize the Sentinel API
    api = SentinelAPI(SCI_HUB_USERNAME, SCI_HUB_PASSWORD, 'https://scihub.copernicus.eu/dhus')
    current_date = date.today()
    first_day_of_previous_month = date(current_date.year, current_date.month - 1, 1)

    # Fetch all areas of interest from the database
    footprints = SciHubAreaInterest.objects.all().order_by('id')

    # For each footprint, query the Sentinel API for relevant images
    for footprint in footprints:
        products = api.query(footprint.polygon.wkt,
                             date=(first_day_of_previous_month.strftime("%Y%m%d"), current_date.strftime("%Y%m%d")),
                             platformname='Sentinel-2',
                             processinglevel='Level-1C',
                             cloudcoverpercentage=(0, 20))

        # If products are found, process them
        if products:
            tiff_coords = []

            # Check each product for valid coordinates and download the first product that meets the condition
            for i in products:
                metadata_product = api.get_product_odata(i)
                check_len_coordinates = len(metadata_product['footprint'].strip("POLYGON((").strip("))").split(","))
                if check_len_coordinates == 5:
                    tiff_coords.append(metadata_product['footprint'])
                    # Download the product and save it to the output directory
                    api.download(products[i]['uuid'], directory_path=output)
                    break
            else:
                # If no products found with valid coordinates, create an entry in the database with a note
                SciHubImageDate.objects.create(area_interest_id=footprint.pk, no_image=True,
                                               note=f'No products found between '
                                                    f'{first_day_of_previous_month.strftime("%Y.%m.%d")} and '
                                                    f'{current_date.strftime("%Y.%m.%d")}')
                continue

            # Continue with the rest of the processing logic if a product was downloaded
            time.sleep(10)
            extract_files(output)
            time.sleep(20)
            for folder in filter(lambda x: x.endswith('.SAFE'), os.listdir(output)):
                convert_and_save_files(output, folder, tiff_coords, footprint)
            time.sleep(15)
            shutil.rmtree(output)  # Clean up the output directory

        else:
            # Create a record indicating no image was found for the given footprint during the time period
            SciHubImageDate.objects.create(area_interest_id=footprint.pk, no_image=True,
                                           note=f'No products found between {first_day_of_previous_month.strftime("%Y.%m.%d")} and {current_date.strftime("%Y.%m.%d")}')

    return Response('Satellite images successfully downloaded.', status=status.HTTP_200_OK)
