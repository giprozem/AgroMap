from threading import Thread

from rest_framework.response import Response
from rest_framework.views import APIView

from indexes.models import ContourAverageIndex, ProductivityClass
from indexes.utils import creating_ndvi


class Creating(APIView):
    def post(self, request, *args, **kwargs):
        date = self.request.query_params['date']
        start = self.request.query_params['start']
        end = self.request.query_params['end']
        thread_object = Thread(target=creating_ndvi, args=(date, int(start), int(end)))
        thread_object.start()
        return Response('started')


class CreatingAverage(APIView):
    def post(self, request, *args, **kwargs):
        from gip.models import Contour
        import json

        response = {}

        for i in range(1135, 1891):
            try:
                contour = Contour.objects.get(id=i)
                pruductivity = ProductivityClass.objects.get(id=1)
                ContourAverageIndex.objects.create(contour=contour, productivity_class=pruductivity)
            except Exception as e:
                response[f'{contour.id}'] = f'{e}'
                pass
            print(contour.id)

        return Response(json.dumps(response))
