from threading import Thread

from rest_framework.response import Response
from rest_framework.views import APIView

from indexes.utils import veg_index_creating


class TestAPIView(APIView):
    def get(self, request):
        thread_object = Thread(target=veg_index_creating)
        thread_object.start()
        return Response('Ok')
