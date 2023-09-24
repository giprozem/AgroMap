from threading import Thread
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from scripts.heat_map_ndvi import run

# API view for running a heat map generation process
class HeatMapAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='do not required for front'
    )
    def get(self, request, *args, **kwargs):
        # Create a new thread to run the heat map generation process
        thread_object = Thread(target=run, args=(request.query_params['year'],))
        thread_object.start()

        return Response('started', status=200)
