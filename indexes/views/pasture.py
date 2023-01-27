from rest_framework.response import Response
from rest_framework.views import APIView

from indexes.models import ContourAverageIndex, ProductivityClass


class Creating(APIView):
    def post(self, request, *args, **kwargs):
        from culture_model.models import VegetationIndex
        from gip.models import Contour
        from indexes.models import ActuaVegIndex
        import json
        index = VegetationIndex.objects.get(id=1)
        # for i in range(1135, 1890):
        date = self.request.query_params['date']
        print(date)
        response = {}
        for i in range(1582, 1891):
            try:
                contour = Contour.objects.get(id=i)
                ActuaVegIndex.objects.create(contour=contour, index=index, date="2022-3-31")
            except Exception as e:
                response[f'{contour.id}'] = f'{e}'
                pass
            print(contour.id)

        return Response(json.dumps(response))


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
