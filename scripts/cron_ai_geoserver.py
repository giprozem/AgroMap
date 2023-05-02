import json
from django.db import connection
from rest_framework.response import Response
import geopandas as gpd


def run():
    with connection.cursor() as cursor:
        cursor.execute(f"""
                        SELECT cntr.id, cntr.district_id, cntr.percent, cntr.culture_id, rgn.id as rgn,
                        cntr.type_id AS land_type_id, cntr.year, cntr.area_ha, cntr.productivity,
                        St_AsGeoJSON(cntr.polygon) as polygon
                        FROM ai_contour_ai as cntr
                        LEFT JOIN gip_landtype AS land ON land.id=cntr.type_id
                        LEFT JOIN gip_district AS dst ON dst.id=cntr.district_id
                        LEFT JOIN gip_region AS rgn ON rgn.id=dst.region_id;
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
        with open('contour_ai.geojson', 'w') as f:
            json.dump(geojson_data, f)

        # Kонвертация GeoJson в Shpfile
        gdf = gpd.read_file('contour_ai.geojson')
        gdf.to_file('shp_ai_contour/agromap_store_ai.shp')

    return Response('OK')
