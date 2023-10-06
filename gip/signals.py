from django.contrib.gis.db.models.functions import Area
from django.db.models.signals import post_save
from django.dispatch import receiver


from gip.models import Contour
from gip.utils.detect_conton import detect_conton
from gip.utils.detect_elevation import calculate_elevation
from gip.utils.detect_soilclass import calculate_soil_class


def detect_conton_handler(is_none: bool, polygon) -> int:
    if is_none:
        pass
    else:
        return detect_conton(polygon=polygon)

# This is a signal handler that responds to the "post_save" signal for the "Contour" model.
@receiver(post_save, sender=Contour)
def update(sender, instance, created, **kwargs):
    try:
        geom = Contour.objects.annotate(area_=Area("polygon")).get(id=instance.id)
        result_soil_class = calculate_soil_class(geom)
        elevation_result = calculate_elevation(geom)
        ha = round(geom.area_.sq_km * 100, 2)

        if created:
            if instance.conton is None:
                conton_id = detect_conton(geom.polygon)
                instance.conton_id = conton_id

            instance.soil_class_id = result_soil_class
            instance.elevation = elevation_result
            instance.area_ha = ha
            instance.save()
        else:
            update_fields = {
                'area_ha': ha,
                'soil_class': result_soil_class,
                'elevation': elevation_result,
            }

            if instance.conton is None:
                conton_id = detect_conton(geom.polygon)
                update_fields['conton_id'] = conton_id

            Contour.objects.filter(id=instance.id).update(**update_fields)
    except Exception as e:
        print(e)
        
        