from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from culture_model.models import Index
from gip.models import Contour
from indexes.models.indexfact import IndexFact
from indexes.serializers.indexfact import IndexFactSerializer


class IndexFactListCreateAPIView(ListAPIView):
    """
    required in request params:
     - contour = id of contour
     - index = id of index
     - date = date of satellite images that have to proces
    """

    def get(self, request, *args, **kwargs):
        response = IndexFact.objects.filter(
            contour=request.query_params['contour']
        ).filter(
            index=request.query_params['index']
        ).filter(
            date=request.query_params['date']
        )

        serializer = IndexFactSerializer(response, many=True)
        return Response(serializer.data, status=200)