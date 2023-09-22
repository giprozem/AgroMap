# For Developers

This project uses the following key scripts and components:

## The scripts directory contains the following files:

1. `cron_download_S2_Copernicus.py` -
   A script set up to automatically download satellite images from Copernicus every month for specified
   areas of interest, hooked up to crontab.
2. `heat_map_ndvi.py`
   A script to create heat maps across the entire territory of Kyrgyzstan, using NDVI index data.
3. `productivity_contour.py`
   A script for a machine learning model that calculates pasture productivity based on downloaded
   satellite images and other data.
4. `productivity_heat_map.py`
   A script to create heat maps of pasture productivity.

## The AI/Utils directory contains the following files:

1. `predicted_contour.py` -
   This script contains a neural network based on YOLOv8 for contour identification based on satellite
   images.

## The Indexes directory contains the following files:

1. `download_satellite_images.py` -
   The script located in the `indexes/views` directory is used for downloading satellite images by the specified date
   and
   area of interest through the `v2/download_satellite_images/` API.
