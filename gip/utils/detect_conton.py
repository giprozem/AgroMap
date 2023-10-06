import logging

from typing import Union

from django.db import connection
from django.contrib.gis.geos import GEOSGeometry


from gip.models.conton import Conton


def detect_conton(polygon: "GEOSGeometry['POLYGON']") -> Union[int, None]:
    """
    find conton using sql queries
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT subquery.name, subquery.id,
                100.0 * ST_Area(ST_Intersection(subquery.polygon, input_polygon.geom)) / ST_Area(subquery.polygon) AS overlap_percentage
                FROM (SELECT dst.name, dst.id, dst.polygon
                      FROM gip_district as dst) AS subquery,
                LATERAL (SELECT '{polygon}'::geometry AS geom) AS input_polygon
                WHERE ST_Intersects(subquery.polygon, input_polygon.geom)
                ORDER BY overlap_percentage DESC
                LIMIT 1;
            """
            )
            conton_id = cursor.fetchall()[0][1] or None
            return conton_id

    except Exception:
        logging.exception("An error occurred while detect conton")
        return None
