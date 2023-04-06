from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from ai.utils.predicted_contour import create_rgb, cut_rgb_tif, merge_bands, deleted_files
from ai.utils.create_dataset import create_dataset
from django.db.models.signals import post_save
from django.dispatch import receiver
from ai.models.create_dataset import Dataset
from notifications.signals import notify


class CreateAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        user = request.user
        # merge_bands()
        # create_rgb()
        # cut_rgb_tif()
        # create_dataset()
        # deleted_files()
        # @receiver(post_save, sender=Dataset)
        # def my_handler(sender, instance, created, **kwargs):
        #     notify.send(instance, recipient=user, verb='was saved')
        return Response({"message": "ok"})
