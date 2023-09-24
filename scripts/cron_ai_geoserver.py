import json
import os
import time

import requests
from decouple import config
from django.db import connection
from rest_framework import status
from rest_framework.response import Response
import geopandas as gpd


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
    output = 'shp_contours_ai/'
    os.makedirs(output, exist_ok=True)  # Create directory if it doesn't exist

    # Establishing a connection to the database and executing SQL query
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
                       )  # Execute SQL to retrieve contour data
        rows = cursor.fetchall()  # Fetch results from the executed SQL
        data = []

        # Constructing a GeoJSON formatted list from database results
        for i in rows:
            data.append(
                {"type": "Feature", "properties": {'id': i[0], 'dst': i[1], 'prt': i[2], 'clt': i[3], 'rgn': i[4],
                                                   'ltype': i[5], 'year': i[6], 'area': i[7], 'prdvty': i[8]},
                 "geometry": eval(i[-1])}
            )

        geojson_data = {"type": "FeatureCollection", "features": data}

        # Save the data in GeoJSON format
        with open('contours_ai_in_geoserver.geojson', 'w') as f:
            json.dump(geojson_data, f)

        # Convert the GeoJSON to a Shapefile format using geopandas
        gdf = gpd.read_file('contours_ai_in_geoserver.geojson')
        gdf.to_file(f'{output}/contours_ai_in_geoserver.shp')

        # Pause the execution to ensure file is saved properly
        time.sleep(5)

        # Setup connection details for the GeoServer REST API
        geoserver_url = f"{config('URL_GEOSERVER')}geoserver/rest"
        username = config('USERNAME_GEOSERVER')
        password = config('PASSWORD_GEOSERVER')

        # Define workspace and data store names for GeoServer
        workspace = 'agromap'
        storename = 'contours_main_ai'
        shapefile_path = output  # Directory path for saved shapefiles

        # Check if workspace exists, if not, create it
        workspace_url = f'{geoserver_url}/workspaces/{workspace}.json'
        workspace_exists = requests.get(workspace_url, auth=(username, password)).ok
        if not workspace_exists:
            requests.post(f'{geoserver_url}/workspaces.json',
                          auth=(username, password),
                          headers={'Content-Type': 'application/json'},
                          json={'workspace': {'name': workspace}})

        # Check if the data store exists, if not, create it
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

        # Upload each shapefile in the directory to the GeoServer data store
        for shpfile_path in os.listdir(shapefile_path):
            shpfile = os.path.basename(shpfile_path)

            with open(f'{shapefile_path}/{shpfile}', 'rb') as f:
                requests.put(f'{store_url}/file.{shpfile[-3:]}?update=overwrite',
                             auth=(username, password),
                             data=f
                             )

        # Publish the shapefile as a new layer on GeoServer
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
