from django.contrib.gis.db.models.functions import Area
from django.db.models.signals import post_save
from django.dispatch import receiver

from gip.models import Contour
from gip.utils.detect_conton import detect_conton
from gip.utils.detect_elevation import calculate_elevation
from gip.utils.detect_soilclass import calculate_soil_class
from gip.utils.formation_veg_indexes import create_veg_indexes
from gip.utils.predicted_cultures import data_contour


def detect_conton_handler(is_none: bool, polygon) -> int:
    if is_none:
        pass
    else:
        return detect_conton(polygon=polygon)


# This is a signal handler that responds to the "post_save" signal for the "Contour" model.
@receiver(post_save, sender=Contour)
def update(sender, instance, created, **kwargs):
    try:
        # Fetch the geometry of the Contour object and calculate its area
        geom = Contour.objects.annotate(area_=Area("polygon")).get(id=instance.id)

        if created:

            create_veg_indexes(geom)  # Call a function to create vegetation indexes

            if instance.conton is None:
                conton_id = detect_conton(geom.polygon)  # Detect a 'conton' ID based on polygon
                instance.conton_id = conton_id  # Set the 'conton' ID in the Contour object

            instance.cadastre = True if instance.eni else False
            instance.soil_class_id = calculate_soil_class(geom)  # Set the soil class in the Contour object
            instance.elevation = calculate_elevation(geom)  # Set the elevation in the Contour object
            instance.area_ha = round(geom.area_.sq_km * 100, 2)  # Set the area in hectares in the Contour object
            instance.save()  # Save the Contour object to the database

        else:
            # If the Contour object is being updated (not created), perform these actions
            update_fields = {
                'area_ha': round(geom.area_.sq_km * 100, 2),  # Update the area in hectares
                'soil_class': calculate_soil_class(geom),  # Update the soil class
                'elevation': calculate_elevation(geom),  # Update the elevation
            }
            if instance.conton is None:
                conton_id = detect_conton(geom.polygon)  # Detect 'conton' ID if not already set
                update_fields['conton_id'] = conton_id  # Update the 'conton' ID if detected

            Contour.objects.filter(id=instance.id).update(**update_fields)  # Update the Contour object fields

        data_contour(geom)
    except Exception as e:
        print(
            f"Error in post_save signal for Contour: {e}")  # Print any exceptions that occur during the update process
