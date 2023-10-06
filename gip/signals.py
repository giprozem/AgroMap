from django.contrib.gis.db.models.functions import Area
from django.db.models.signals import post_save
from django.dispatch import receiver


from gip.models import Contour
from gip.utils.detect_conton import detect_conton
from gip.utils.detect_elevation import calculate_elevation
from gip.utils.detect_soilclass import calculate_soil_class


# This is a signal handler that responds to the "post_save" signal for the "Contour" model.
@receiver(post_save, sender=Contour)
def update(sender, instance, created, **kwargs):
    geom = Contour.objects.annotate(area_=Area("polygon")).get(id=instance.id)
    # conton_id = detect_conton(geom.polygon)
    if created:
        result_soil_class = calculate_soil_class(geom)
        elevation_result = calculate_elevation(geom)
        ha = round(geom.area_.sq_km * 100, 2)
        instance.soil_class_id = result_soil_class
        # instance.conton_id = conton_id
        instance.elevation = elevation_result
        instance.area_ha = ha
        instance.save()
    else:
        result_soil_class = calculate_soil_class(geom)
        elevation_result = calculate_elevation(geom)
        ha = round(geom.area_.sq_km * 100, 2)
        Contour.objects.filter(id=instance.id).update(area_ha=ha, soil_class=result_soil_class, elevation=elevation_result)