from django.contrib.gis.db.models.functions import Area
from django.db.models.signals import post_save
from django.dispatch import receiver
from shapely.wkt import loads
import requests
from django.contrib.gis.geos import Point

from gip.models import ContourYear, Elevation


# @receiver(post_save, sender=ContourYear)
# def update(sender, instance, created, **kwargs):
#     if created:
#         geom = ContourYear.objects.annotate(area_=Area("polygon")).get(id=instance.id)
#         center = loads(f"{geom.polygon.centroid}".strip('SRID=4326;'))
#         x, y = center.x, center.y
#         result_elevation = \
#             requests.get(f"https://api.opentopodata.org/v1/gebco2020?locations={y},{x}").json()['results'][0][
#                 'elevation']
#         Elevation.objects.create(point=Point(x, y), elevation=result_elevation)
#         ha = round(geom.area_.sq_km * 100, 2)
#         instance.area_ha = ha
#         instance.elevation = result_elevation
#         instance.save()
#     else:
#         geom = ContourYear.objects.annotate(area_=Area("polygon")).get(id=instance.id)
#         center = loads(f"{geom.polygon.centroid}".strip('SRID=4326;'))
#         x, y = center.x, center.y
#         result_elevation = \
#             requests.get(f"https://api.opentopodata.org/v1/gebco2020?locations={y},{x}").json()['results'][0][
#                 'elevation']
#         ha = round(geom.area_.sq_km * 100, 2)
#         ContourYear.objects.filter(id=instance.id).update(area_ha=ha, elevation=result_elevation)
