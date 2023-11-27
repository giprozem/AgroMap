# Importing necessary libraries
import json
import os
import time
import requests
from django.db import connection
from rest_framework import status
from rest_framework.response import Response
import geopandas as gpd
from decouple import config


def run():
    """
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
    """

    # Creating an output directory
    output = 'shp_contours/'
    os.makedirs(output, exist_ok=True)
    # Establishing a connection to the database
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT CASE WHEN (cntr.productivity)::float >= 1.6 THEN 1 ELSE 0 END AS "Type productivity",
        cntr.id AS contour_year_id, rgn.id as rgn, dst.id as dst, cntn.id as cntn, coalesce(cl.name_en, NULL) AS cl_name_en,
        cntr.type_id AS land_type_id, cntr.year, cntr.area_ha, cntr.productivity, cntr.cadastre, 
        St_AsGeoJSON(cntr.polygon) as polygon
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
                                                           'prd_clt': i[5], 'ltype': i[6], 'year': i[7], 'area': i[8],
                                                           'cdstr': i[-2],
                                                           'prdvty': i[0]},
                         "geometry": eval(i[-1])})

        # Creating a GeoJSON FeatureCollection with the list of features
        geojson_data = {"type": "FeatureCollection", "features": data}

        # Saving the GeoJSON data into a file
        with open('contours_in_geoserver.geojson', 'w') as f:
            json.dump(geojson_data, f)

        # Converting the GeoJSON file into a Shapefile using GeoPandas
        gdf = gpd.read_file('contours_in_geoserver.geojson')
        gdf.to_file(f'{output}/contours_in_geoserver.shp')

        # Delay to allow the system to process the file
        time.sleep(5)
        # Establishing a connection to GeoServer using REST API
        geoserver_url = f"{config('URL_GEOSERVER')}geoserver/rest"

        # Defining credentials for authentication
        username = config('USERNAME_GEOSERVER')
        password = config('PASSWORD_GEOSERVER')

        # Defining the workspace and store names
        workspace = 'agromap'
        storename = 'contours_main'

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

    return Response({"message": "Successfully processed and uploaded data to GeoServer."}, status=status.HTTP_200_OK)
