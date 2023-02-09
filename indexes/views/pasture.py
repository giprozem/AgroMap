from threading import Thread

from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import ContourYear
from indexes.models import ContourAverageIndex, ProductivityClass
from indexes.utils import creating_ndvi


class Creating(APIView):
    def post(self, request, *args, **kwargs):
        """
        required query_params:
        - date
        - start
        - end
        """
        date = self.request.query_params['date']
        start = self.request.query_params['start']
        end = self.request.query_params['end']
        indexid = self.request.query_params['indexid']
        thread_object = Thread(target=creating_ndvi, args=(date, int(start), int(end), int(indexid)))
        thread_object.start()
        return Response('started')


class CreatingAverage(APIView):
    def post(self, request, *args, **kwargs):
        """
        required query_params:
        - date
        - start
        - end
        """

        start = self.request.query_params['start']
        end = self.request.query_params['end']

        for i in range(int(start), int(end)):
            try:
                contour = ContourYear.objects.get(id=i)
                pruductivity = ProductivityClass.objects.get(id=1)
                ContourAverageIndex.objects.create(contour=contour, productivity_class=pruductivity)
            except Exception as e:
                with open(f'reportCreatingAverage.txt', 'a') as file:
                    file.write(f"{i}' = f'{e}")
                    file.write(',')
                    file.write('\n')
                pass

        return Response('started')
