import json
import os
import time
import requests
from django.db import connection
from rest_framework.response import Response
import geopandas as gpd
from decouple import config


def run():
    with connection.cursor() as cursor:
        cursor.execute(f"""
                        SELECT cntr.id, cntr.district_id, cntr.percent, cntr.culture
                        FROM ai_contour_ai as cntr
                        WHERE cntr.id > 11016;
                        """
                       )
        rows = cursor.fetchall()
        data = []
        for i in rows:
            data.append({"type": "Feature", "properties": {'id': i[0], 'dst': i[1], 'prt': i[2], 'clt': i[3]},
                         "geometry": eval(i[-1])})

        geojson_data = {"type": "FeatureCollection", "features": data}


        # Сохранение в geojson
        with open('contour_ai.geojson', 'w') as f:
            json.dump(geojson_data, f)

        # Kонвертация GeoJson в Shpfile
        gdf = gpd.read_file('contour_ai.geojson')
        gdf.to_file('shp_ai_contour/polygons.shp')

        time.sleep(5)
        # GeoServer REST API
        geoserver_url = f"{config('URL_GEOSERVER')}geoserver/rest"

        # Учетные данные для аутентификации
        username = config('USERNAME_GEOSERVER')
        password = config('PASSWORD_GEOSERVER')

        # Рабочее пространство и хранилище
        workspace = 'agromap'
        storename = 'agromap_store_ai'

        # Путь к папке с файлами
        shapefile_path = 'shp_ai_contour'

        # Создание рабочую область, если она еще не существует
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

        # Загрузка каждого файла в папке
        for shpfile_path in os.listdir(shapefile_path):
            shpfile = os.path.basename(shpfile_path)

            with open(f'{shapefile_path}/{shpfile}', 'rb') as f:
                requests.put(f'{store_url}/file.{shpfile[-3:]}?update=overwrite',
                             auth=(username, password),
                             data=f
                             )

        # Опубликация слоя на GeoServer
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

    return Response('OK')
