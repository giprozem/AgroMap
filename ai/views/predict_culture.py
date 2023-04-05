from threading import Thread

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.utils.predicting_culture import predicting_culture


class CulturePredict(APIView):
    @swagger_auto_schema(
        operation_summary='do not required for front',
        operation_description='predicting culture in given satellite image id'
    )
    def get(self, request, *args, **kwargs):
        thread_obj = Thread(target=predicting_culture, args=(request.query_params['satellite_id'],))
        thread_obj.start()
        return Response('result', status=200)
