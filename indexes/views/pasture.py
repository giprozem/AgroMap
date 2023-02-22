from threading import Thread

import matplotlib.pyplot as plt
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import ContourYear
from indexes.models import ContourAverageIndex, ProductivityClass
from indexes.utils import creating_indexes


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
                    plt.close()
                pass

        return Response('started')


class AllIndexesCreating(APIView):

    def post(self, request, *args, **kwargs):
        """
        required query_params:
        - date
        - satellite_image_id
        """
        date = self.request.query_params['date']
        satellite_image_id = self.request.query_params['satellite_image_id']

        thread_object = Thread(target=creating_indexes, args=(date, satellite_image_id))
        thread_object.start()

        return Response('AllIndexesCreating')
