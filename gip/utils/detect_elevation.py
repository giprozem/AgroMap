from elevation.data import elevation

import logging

from typing import Union

from django.db.models import QuerySet

from shapely.wkt import loads

from gip.models.contour import Contour


def calculate_elevation(geom: QuerySet[Contour]) -> Union[int, None]:
    try:
        center = loads(f"{geom.polygon.centroid}".strip('SRID=4326;'))
        x, y = center.x, center.y
        elevation_result = elevation(latitude=y, longitude=x)

        return elevation_result
    
    except Exception as e:
        logging.exception("An error occurred while calculating elevation")
        return None
