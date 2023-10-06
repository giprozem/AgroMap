import logging

from typing import Union

from django.db import connection
from django.db.models import QuerySet
from django.contrib.gis.geos import GEOSGeometry


from gip.models.contour import Contour


def calculate_soil_class(geom: QuerySet[Contour]) -> Union[int, None]:
    try:
        polygon: GEOSGeometry = geom.polygon
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                    SELECT subquery.name, subquery.id, subquery.soil_id, subquery.percent
                    FROM (
                        SELECT ST_Area(ST_Intersection(scm.polygon::geometry,
                        '{polygon}'::geography::geometry)) / ST_Area(scm.polygon::geometry) * 100 as percent,
                        sc.id, sc.name, scm.id as soil_id
                        FROM gip_soilclassmap as scm
                        JOIN gip_soilclass as sc
                        ON sc.id = scm.soil_class_id
                    ) as subquery
                    ORDER BY subquery.percent DESC
                    LIMIT 1;
                """
            )
            rows = cursor.fetchall()
            result_soil_class = rows[0][1] if rows != [] else None
        return result_soil_class

    except Exception as e:
        logging.exception("An error occurred while calculating soil class")
        return None
