from threading import Thread

from django.db.models.signals import post_save
from django.dispatch import receiver

from indexes.models.satelliteimage import SatelliteImages
from indexes.utils import creating_ndvi


@receiver(post_save, sender=SatelliteImages)
def creating_ndvi_post_save(sender, instance, created, **kwargs):
    if created:
        thread_object = Thread(target=creating_ndvi, args=(instance.date, 1135, 1891))
        thread_object.start()
