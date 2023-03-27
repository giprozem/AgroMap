from threading import Thread

from django.db.models.signals import post_save
from django.dispatch import receiver

from indexes.models.satelliteimage import SciHubImageDate
from indexes.utils import creating_veg_index_to_given_image


@receiver(post_save, sender=SciHubImageDate)
def creating_indexes_to_uploaded_image(sender, instance, created, **kwargs):
    if created:
        thread_obj = Thread(target=creating_veg_index_to_given_image, args=(instance,))
        thread_obj.start()
