import json
import os
import time

import requests
from decouple import config
from django.db import connection
from rest_framework.response import Response
import geopandas as gpd


def run():
    # Creating an output directory
    output = 'shp_contours_ai/'
    os.makedirs(output, exist_ok=True)
    # Establishing a connection to the database
    with connection.cursor() as cursor:
        cursor.execute(f"""
                        SELECT cntr.id, cntr.district_id, cntr.percent, cntr.culture_id, rgn.id as rgn,
                        cntr.type_id AS land_type_id, cntr.year, cntr.area_ha, cntr.productivity,
                        St_AsGeoJSON(cntr.polygon) as polygon
                        FROM ai_contour_ai as cntr
                        LEFT JOIN gip_landtype AS land ON land.id=cntr.type_id
                        LEFT JOIN gip_district AS dst ON dst.id=cntr.district_id
                        LEFT JOIN gip_region AS rgn ON rgn.id=dst.region_id
                        WHERE cntr.is_deleted=False;
                        """
                       )
        rows = cursor.fetchall()
        data = []

        for i in rows:
            data.append({"type": "Feature", "properties": {
                    'id': i[0],
                    'dst': i[1],
                    'prt': i[2],
                    'clt': i[3],
                    'rgn': i[4],
                    'ltype': i[5],
                    'year': i[6],
                    'area': i[7],
                    'prdvty': i[8]
                    },
                         "geometry": eval(i[-1])
                         }
                        )

        geojson_data = {"type": "FeatureCollection", "features": data}


        # Сохранение в geojson
        with open('contours_ai_in_geoserver.geojson', 'w') as f:
            json.dump(geojson_data, f)

        # Kонвертация GeoJson в Shpfile
        gdf = gpd.read_file('contours_ai_in_geoserver.geojson')
        gdf.to_file(f'{output}/contours_ai_in_geoserver.shp')

        # Delay to allow the system to process the file
        time.sleep(5)
        # Establishing a connection to GeoServer using REST API
        geoserver_url = f"{config('URL_GEOSERVER')}geoserver/rest"

        # Defining credentials for authentication
        username = config('USERNAME_GEOSERVER')
        password = config('PASSWORD_GEOSERVER')

        # Defining the workspace and store names
        workspace = 'agromap'
        storename = 'contours_main_ai'

        # Defining the path to the folder containing the files
        shapefile_path = output

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
                                  'url': f'file:data_dir/workspaces/agromap/{shapefile_path}',
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

    return Response('OK')
