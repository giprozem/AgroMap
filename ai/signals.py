from django.contrib.gis.db.models.functions import Area
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver
from elevation.data import elevation
from shapely.wkt import loads
from ai.models.predicted_contour import Contour_AI
from ai.models.create_dataset import *
from ai.utils.create_dataset import create_dataset
from ai.utils.predicted_contour import predicted_contour


@receiver(post_save, sender=Contour_AI)
def update(sender, instance, created, **kwargs):
    """
    The post_save signal for the Cut_RGB_TIF model in this case does the following:
    When saving (or creating) a Cut_RGB_TIF instance, the signal checks the value of the type_of_process field of that instance.
    If the value of type_of_process is 1, then this means that the "predicted_contour" process was selected. In this case, 
    the signal calls the predicted_contour() function, which probably performs contour detection of objects in images.
    If the value of type_of_process is 2, then this means that the "create_dataset" process was selected. In this case, 
    the signal calls the create_dataset() function, which probably creates the dataset.
    """
    if created:
        geom = Contour_AI.objects.annotate(area_=Area("polygon")).get(id=instance.id)
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
        instance.soil_class_id = result_soil_class
        center = loads(f"{geom.polygon.centroid}".strip('SRID=4326;'))
        x, y = center.x, center.y
        elevation_result = elevation(latitude=y, longitude=x)
        ha = round(geom.area_.sq_km * 100, 2)
        instance.elevation = elevation_result
        instance.area_ha = ha
        instance.save()
    else:
        geom = Contour_AI.objects.annotate(area_=Area("polygon")).get(id=instance.id)
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
        Contour_AI.objects.filter(id=instance.id).update(area_ha=ha, soil_class_id=result_soil_class,
                                                         elevation=elevation_result)


@receiver(post_save, sender=Cut_RGB_TIF)
def choice_handler(sender, instance, created, **kwargs):
    if created:
        match instance.type_of_process:
            case 1:
                predicted_contour()
            case 2:
                create_dataset()