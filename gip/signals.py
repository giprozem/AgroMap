from django.contrib.gis.db.models.functions import Area
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver
from shapely.wkt import loads
from gip.models import Contour
from elevation.data import elevation

# This is a signal handler that responds to the "post_save" signal for the "Contour" model.
@receiver(post_save, sender=Contour)
def update(sender, instance, created, **kwargs):
    if created:
        # Calculate the area of the contour's polygon.
        geom = Contour.objects.annotate(area_=Area("polygon")).get(id=instance.id)
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT subquery.name, subquery.id, subquery.soil_id, subquery.percent
                FROM (
                    SELECT ST_Area(ST_Intersection(scm.polygon::geometry,
                    '{geom.polygon}'::geography::geometry)) / ST_Area(scm.polygon::geometry) * 100 as percent,
                    sc.id, sc.name, scm.id as soil_id
                    FROM gip_soilclassmap as scm
                    JOIN gip_soilclass as sc
                    ON sc.id = scm.soil_class_id
                ) as subquery
                ORDER BY subquery.percent DESC
                LIMIT 1;
            """)
            rows = cursor.fetchall()
            result_soil_class = rows[0][1] if rows != [] else None

        # Calculate the contour's elevation using external data.
        center = loads(f"{geom.polygon.centroid}".strip('SRID=4326;'))
        x, y = center.x, center.y
        elevation_result = elevation(latitude=y, longitude=x)

        # Calculate the area in hectares.
        ha = round(geom.area_.sq_km * 100, 2)

        # Update the instance's fields and save it.
        instance.soil_class_id = result_soil_class
        instance.elevation = elevation_result
        instance.area_ha = ha
        instance.save()
    else:
        # Similar calculations and updates for an existing contour.
        geom = Contour.objects.annotate(area_=Area("polygon")).get(id=instance.id)
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT subquery.name, subquery.id, subquery.soil_id, subquery.percent
                FROM (
                    SELECT ST_Area(ST_Intersection(scm.polygon::geometry,
                    '{geom.polygon}'::geography::geometry)) / ST_Area(scm.polygon::geometry) * 100 as percent,
                    sc.id, sc.name, scm.id as soil_id
                    FROM gip_soilclassmap as scm
                    JOIN gip_soilclass as sc
                    ON sc.id = scm.soil_class_id
                ) as subquery
                ORDER BY subquery.percent DESC
                LIMIT 1;
            """)
            rows = cursor.fetchall()
            result_soil_class = rows[0][1] if rows != [] else None

        center = loads(f"{geom.polygon.centroid}".strip('SRID=4326;'))
        x, y = center.x, center.y
        elevation_result = elevation(latitude=y, longitude=x)

        ha = round(geom.area_.sq_km * 100, 2)

        # Update the fields of the existing contour and save it.
        Contour.objects.filter(id=instance.id).update(area_ha=ha, soil_class_id=result_soil_class, elevation=elevation_result)
