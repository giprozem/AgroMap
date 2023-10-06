import os
from threading import Thread

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from gip.models.contour import Contour
from indexes.models.actual_veg_index import ActualVegIndex
from indexes.models.actual_veg_index_logs import IndexCreatingReport
from indexes.models.satelliteimage import SciHubImageDate
from indexes.utils import veg_index_creating


@receiver(post_save, sender=SciHubImageDate)
def creating_indexes_to_uploaded_image(sender, instance, created, **kwargs):
    """
    Signal handler that gets executed post the saving of a SciHubImageDate instance. If the instance was created,
    it spawns a new thread to create vegetation indices based on the uploaded image.
    """

    if created:
        thread_obj = Thread(target=veg_index_creating, args=(instance, Contour, IndexCreatingReport, ActualVegIndex))
        thread_obj.start()


@receiver(post_delete, sender=ActualVegIndex)
def delete_index_image(sender, instance, **kwargs):
    # Check if the instance has an attribute index_image.
    if instance.index_image:

        # Check if the file pointed by index_image.path exists.
        if os.path.isfile(instance.index_image.path):
            # Remove the file from the file system.
            os.remove(instance.index_image.path)
