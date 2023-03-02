import json
import os
import time

import requests
from rest_framework.response import Response
from rest_framework.views import APIView
import geopandas as gpd

from decouple import config
from gip.models import ContourYear


class Geoserver(APIView):
    def get(self, request, *args, **kwargs):
        data = []

        # Извлечение из бд геоданных
        for i in ContourYear.objects.all():
            data.append({"type": "Feature", "properties": {"id_contour_year": i.id, "type": i.type.id},
                         "geometry": eval(i.polygon.geojson)})
        geojson_data = {"type": "FeatureCollection", "features": data}

        # Сохранение в geojson
        with open('polygons.geojson', 'w') as f:
            json.dump(geojson_data, f)

        # Kонвертация GeoJson в Shpfile
        gdf = gpd.read_file('polygons.geojson')
        gdf.to_file('shp/polygons.shp')

        time.sleep(5)
        # GeoServer REST API
        geoserver_url = f"{config('URL_GEOSERVER')}geoserver/rest"

        # Учетные данные для аутентификации
        username = config('USERNAME_GEOSERVER')
        password = config('PASSWORD_GEOSERVER')

        # Рабочее пространство и хранилище
        workspace = 'agromap'
        storename = 'agromap_store'

        # Путь к шейп-файлу
        shapefile_path = 'shp/polygons.shp'

        # Создание рабочую область, если она еще не существует
        workspace_url = f'{geoserver_url}/workspaces/{workspace}.json'
        workspace_exists = requests.get(workspace_url, auth=(username, password)).ok

        if not workspace_exists:
            requests.post(f'{geoserver_url}/workspaces.json',
                          auth=(username, password),
                          headers={'Content-Type': 'application/json'},
                          json={'workspace': {'name': workspace}})

        # Создание хранилище, если она еще не существует
        store_url = f'{geoserver_url}/workspaces/{workspace}/datastores/{storename}.json'
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
        shpfile = os.path.basename(shapefile_path)
        shpfile_no_ext = os.path.splitext(shpfile)[0]

        with open(f'{shapefile_path}', 'rb') as f:
            requests.put(f'{store_url}/file.shp?update=overwrite',
                         auth=(username, password),
                         data=f
                         )

        # Опубликация слой на GeoServer
        layer_url = f'{geoserver_url}/workspaces/{workspace}/datastores/{storename}/featuretypes.json'
        layer_name = shpfile_no_ext

        requests.post(layer_url,
                      auth=(username, password),
                      headers={'Content-Type': 'application/json'},
                      json={'featureType': {
                          'name': layer_name,
                          'nativeName': layer_name,
                          'title': layer_name,
                          'srs': 'EPSG:4326'
                      }})

        return Response('OK')
