# Importing necessary libraries
import json
import os
import shutil
import time
import requests
from django.db import connection
from rest_framework.response import Response
import geopandas as gpd
from decouple import config

def run():
    # Creating an output directory
    output = 'shp_contour_productivity/'
    os.makedirs(output, exist_ok=True)

    # Establishing a connection to the database
    with connection.cursor() as cursor:
        # Executing a SQL query to select required data from various tables of the database
        # ... (SQL query continues as in your function)
        # Fetching all rows
        rows = cursor.fetchall()

        # Creating a list to hold the data
        data = []
        # Looping over each row in the fetched data
        for i in rows:
            # Appending each row's data as a GeoJSON Feature
            data.append({"type": "Feature", "properties": {'id': i[1], 'rgn': i[2], 'dst': i[3], 'cntn': i[4],
                                                           'clt': i[5], 'ltype': i[6], 'year': i[7], 'area': i[8],
                                                           'prdvty': i[0]},
                         "geometry": eval(i[-1])})

        # Creating a GeoJSON FeatureCollection with the list of features
        geojson_data = {"type": "FeatureCollection", "features": data}

        # Saving the GeoJSON data into a file
        with open('agromap_store.geojson', 'w') as f:
            json.dump(geojson_data, f)

        # Converting the GeoJSON file into a Shapefile using GeoPandas
        gdf = gpd.read_file('agromap_store.geojson')
        gdf.to_file(f'{output}/agromap_store.shp')

        # Delay to allow the system to process the file
        time.sleep(5)
        # Establishing a connection to GeoServer using REST API
        geoserver_url = f"{config('URL_GEOSERVER')}geoserver/rest"

        # Defining credentials for authentication
        username = config('USERNAME_GEOSERVER')
        password = config('PASSWORD_GEOSERVER')

        # Defining the workspace and store names
        workspace = 'agromap'
        storename = 'agromap_store'

        # Defining the path to the folder containing the files
        shapefile_path = 'shp'

        # Creating workspace if it does not exist
        workspace_url = f'{geoserver_url}/workspaces/{workspace}.json'
        workspace_exists = requests.get(workspace_url, auth=(username, password)).ok

        if not workspace_exists:
            requests.post(f'{geoserver_url}/workspaces.json',
                          auth=(username, password),
                          headers={'Content-Type': 'application/json'},
                          json={'workspace': {'name': workspace}})

        # Создание хранилище, если она еще не существует
        store_url = f'{geoserver_url}/workspaces/{workspace}/datastores/{storename}'
        store_exists = requests.get(store_url, auth=(username, password)).ok

        if not store_exists:
            requests.post(f'{geoserver_url}/workspaces/{workspace}/datastores.json',
                          auth=(username, password),
                          headers={'Content-Type': 'application/json'},
                          json={'dataStore': {
                              'name': storename,
                              'type': 'Shapefile',
                              'enabled': True,
                              'connectionParameters': {
                                  'url': f'file:data/agromap/{shapefile_path}',
                                  'create spatial index': True
                              }
                          }})

        # Loading each file in the folder
        for shpfile_path in os.listdir(shapefile_path):
            shpfile = os.path.basename(shpfile_path)

            with open(f'{shapefile_path}/{shpfile}', 'rb') as f:
                requests.put(f'{store_url}/file.{shpfile[-3:]}?update=overwrite',
                             auth=(username, password),
                             data=f
                             )

        # Publishing the layer on GeoServer
        layer_url = f'{geoserver_url}/workspaces/{workspace}/datastores/{storename}'
        layer_name = 'polygons'

        requests.post(layer_url,
                      auth=(username, password),
                      headers={'Content-Type': 'application/json'},
                      json={'featureType': {
                          'name': layer_name,
                          'nativeName': layer_name,
                          'title': layer_name,
                          'srs': 'EPSG:4326',
                          'type': 'ESRI Shapefile'
                      }})

        # Removing the output directory after use
        shutil.rmtree(output)

    return Response('OK')
