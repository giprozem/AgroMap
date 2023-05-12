from threading import Thread

from rest_framework.response import Response
from rest_framework.views import APIView

from indexes.utils import create_veg_indexes
from drf_yasg.utils import swagger_auto_schema


class CreatingVegIndexesAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='do not required for front'
    )
    def get(self, request):
        thread_object = Thread(target=create_veg_indexes)
        thread_object.start()
        return Response('Ok')
