from threading import Thread

from rest_framework.response import Response
from rest_framework.views import APIView

from indexes.utils import download_satellite_images_v2


class DownloadSatelliteImagesV2(APIView):

    def get(self, request):
        thread_object = Thread(target=download_satellite_images_v2)
        thread_object.start()
        return Response('OK')

