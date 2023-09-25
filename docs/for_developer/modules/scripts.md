# 📂 **Scripts Directory Structure**

-----

#### This directory structure contains scripts for various tasks related to satellite image processing, GeoServer integration, and image download and processing.

```
📁 **scripts**
├── 📁 Satellite Image Processing
│ ├── 📄 create_veg_indexes_ai.py
│ ├── 📄 create_veg_indexes_gip.py
│ ├── 📄 heat_map_ndvi.py
│ └── 📄 productivity_contour.py

├── 📁 GeoServer Integration
│ ├── 📄 cron_ai_geoserver.py
│ └── 📄 cron_geoserver.py

└── 📁 Image Download & Processing
├── 📄 cron_download_S2_Copernicus.py
```


#### 📁 **Satellite Image Processing**

--------------- 

📄 [create_veg_indexes_ai.py](/scripts/create_veg_indexes_ai.py)

```
This module provides functionality to create vegetation indices for satellite images.
Create vegetation indices for a given satellite image and store them in the database.
It also generates reports of successful and unsuccessful index creations.

Parameters:
- satellite_image (Model instance): The satellite image to be processed.
- contour_obj (Django Model): The model representing the contours of interest.
- creating_report_obj (Django Model): The model used for storing processing reports.
- veg_index_obj (Django Model): The model representing vegetation index values.
```

📄 [create_veg_indexes_gip.py](/scripts/create_veg_indexes_gip.py)

```
The script aims to process satellite images, stored in a model SciHubImageDate, in parallel.
It uses a utility function veg_index_creating to create a vegetation index for each satellite image.
This utility function is expected to interact with multiple models,
including Contour, IndexCreatingReport, and ActualVegIndex.
```

📄 [heat_map_ndvi.py](/scripts/heat_map_ndvi.py)

```
This script processes satellite images of specific areas of interest to extract and store NDVI (Normalized Difference Vegetation Index) data for a specific year. Here is a detailed description of what each function does and the main sequence of actions:

- get_tiles(ds, width=50, height=50): This function splits the data into tiles of the specified width and height.

- cropping(in_path, out_path, output_filename, date): The function uses the get_tiles() function to crop a satellite image into many small images or "tiles".

- get_epsg(ref): Determines the EPSG code based on a spatial reference.

- get_center_point(file_path): Returns the center coordinates (longitude and latitude) of the given raster file.

- response_convert_shape_file(...): Converts a JSON response (containing coordinates and NDVI data) to GeoJSON format and saves it to a file.

- convert_shape_to_tif(...): Converts a shapefile to TIFF format.

- creating_folder(creating_folder_name): Creates a folder with the specified name if it does not exist.

- merge_df(links): Merges multiple CSV files into one DataFrame.

- run(year=datetime.datetime.now().year): This is the main function that processes satellite images:

  - It starts by querying all areas of interest.
  - For each area of interest, satellite images are then filtered by date.
  - For each filtered image, the B04 and B8A channels are cropped.
  - After channel trimming, NDVI is calculated for each pair of images.
  - Temporary folders and files are deleted and the NDVI data is saved to a CSV file.
  - All CSV files are combined into one file.
  - The resulting data is then converted into various formats.
```

📄 [productivity_contour.py](/scripts/productivity_contour.py)

```
Load a pre-trained model from a pickle file and annotate contours with their average vegetation index value.

This function performs the following operations:

1. Filters the Contour objects based on certain criteria.
2. Annotates these objects with the average vegetation index value.
3. Loads a pre-trained model from a pickle file.
```

#### 📁 **GeoServer Integration**

---------------

📄 [cron_ai_geoserver.py](/scripts/cron_ai_geoserver.py)

```
1 - Extract Data from a Database:
It connects to a database and executes a SQL query to fetch data related to various geographical contours
and their attributes.
The returned data is structured into GeoJSON format.

2 - Save Data to Files:
The script then saves the data in GeoJSON format to a file (contours_ai_in_geoserver.geojson).
Using the geopandas library, this GeoJSON file is then converted into a shapefile (contours_ai_in_geoserver.shp)
and saved in a specific directory (shp_contours_ai/).

3 - Integration with GeoServer:
After a brief delay, the script establishes a connection with GeoServer using its REST API.
GeoServer is a server that allows for sharing, processing, and editing geospatial data.
It then checks if specific workspaces and data stores exist on the GeoServer. If not, they are created.
The script then uploads the shapefile from the shp_contours_ai/ directory to the GeoServer data store.
Finally, a new layer named 'polygons' is published on the GeoServer using the uploaded shapefile.

```

📄 [cron_geoserver.py](/scripts/cron_geoserver.py)

```
1 - Extract Data from a Database:
It connects to a database and executes a SQL query to fetch data related to various geographical contours
and their attributes.
The returned data is structured into GeoJSON format.

2 - Save Data to Files:
The script then saves the data in GeoJSON format to a file (contours_in_geoserver.geojson).
Using the geopandas library, this GeoJSON file is then converted into a shapefile (contours_in_geoserver.shp)
and saved in a specific directory (shp_contours/).

3 - Integration with GeoServer:
After a brief delay, the script establishes a connection with GeoServer using its REST API.
GeoServer is a server that allows for sharing, processing, and editing geospatial data.
It then checks if specific workspaces and data stores exist on the GeoServer. If not, they are created.
The script then uploads the shapefile from the shp_contours/ directory to the GeoServer data store.
Finally, a new layer named 'polygons' is published on the GeoServer using the uploaded shapefile.
```

#### 📁 **Image Download & Processing**

--------------- 

📄 [cron_download_S2_Copernicus.py](/scripts/cron_download_S2_Copernicus.py)

```
This script is designed to extract, process and save Sentinel-2 satellite images for all regions of interest.

Main features of the script:

- Setting up the Sentinel Hub API:
  The API is initialized to access Sentinel Hub using the provided credentials (login and password).

- Request to Sentinel API:
  For each area of interest (footprint) from the database, a query is made to the Sentinel API to obtain Sentinel-2 satellite imagery for the last month with less than 20% cloud cover.
  If additional products are found in this area, they are loaded, processed and main.

- Image processing:
  Downloaded images are extracted from the archive.
  Images in JP2 format are converted to TIFF format.
  Satellite image metadata (for example, creation date) is located in the SciHubImageDate model database.

- Exception Handling:
  If no images are found for a given region of interest within a given time period, an entry is created in the database indicating that no image was found with an appropriate note.

- Cleaning:
  After processing each area of interest, the temporary folder for downloaded images is cleared.

- Answer:
  After all operations are completed, the script returns a response indicating that the image was successfully loaded.

- Additional functions:
  - extract_files: Extracts all ZIP files in the specified directory.
  - Convert_jp2_to_tif: Converts files from JP2 format to TIFF format using the GDAL library.
  - Convert_and_save_files: Converts JP2 files to TIFF format and saves satellite image metadata in a database.
```