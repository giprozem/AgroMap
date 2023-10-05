from django.db import connection

from gip.models.conton import Conton

def detect_conton(polygon) -> int:
    print(polygon)
    """
    find conton using sql queries
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT scm.id, 
                (ST_Area(ST_Intersection(scm.polygon::geometry, '{polygon}'::geometry)) / ST_Area(scm.polygon::geometry)) * 100 AS similarity_percentage
                FROM gip_conton AS scm
                ORDER BY similarity_percentage DESC
                LIMIT 1;

            """
            )
            conton_id = cursor.fetchall()[0][1]
            print(conton_id)
            return conton_id

    except Exception as e:
        print(f"Error in detect_conton: {e}")
        return None