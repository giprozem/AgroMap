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
        cursor.execute(f"""SELECT CASE WHEN (cntr.productivity)::float >= 1.6 THEN 1 ELSE 0 END AS "Type productivity",
        cntr.id AS contour_year_id, rgn.id as rgn, dst.id as dst, cntn.id as cntn, coalesce(cl.id, NULL) AS cl_id,
        cntr.type_id AS land_type_id, cntr.year, cntr.area_ha, cntr.productivity, St_AsGeoJSON(cntr.polygon) as polygon
        FROM gip_contour AS cntr
        JOIN gip_landtype AS land ON land.id=cntr.type_id
        JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
        JOIN gip_district AS dst ON dst.id=cntn.district_id
        JOIN gip_region AS rgn ON rgn.id=dst.region_id
        LEFT JOIN gip_cropyield as cy ON cy.contour_id = cntr.id
        LEFT JOIN gip_culture as cl ON cy.culture_id = cl.id
        WHERE cntr.is_deleted=False
        GROUP BY "Type productivity", cntr.id, rgn.id, dst.id, cntn.id, land.id, cl.id;""")
        rows = cursor.fetchall()
        data = []
        for i in rows:
            data.append({"type": "Feature", "properties": {'id': i[1], 'rgn': i[2], 'dst': i[3], 'cntn': i[4],
                                                           'clt': i[5], 'ltype': i[6], 'year': i[7], 'area': i[8],
                                                           'prdvty': i[0]},
                         "geometry": eval(i[-1])})

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

        # Путь к папке с файлами
        shapefile_path = 'shp'

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
