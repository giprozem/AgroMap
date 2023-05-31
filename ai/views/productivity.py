from rest_framework.response import Response
from rest_framework.views import APIView

from ai.models import Contour_AI
from ai.productivity_funcs.predicting import productivity_predict
from indexes.models import PredictedContourVegIndex


class PredictingProductivityAPIVie(APIView):

    def get(self, request, *args, **kwargs):
        veg = PredictedContourVegIndex.objects.filter(index_id=1, date='2022-06-21')
        for i in veg:
            result = productivity_predict(float(i.average_value))
            if result <= 0:
                result = 0
            contour = Contour_AI.objects.get(id=i.contour.id)
            contour.productivity = round(result, 3)
            contour.save()
            print(i.contour.id)
        return Response('ok', status=200)
