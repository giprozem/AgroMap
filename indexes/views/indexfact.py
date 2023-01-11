from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from culture_model.models import Index
from gip.models import Contour
from indexes.models.indexfact import IndexFact
from indexes.serializers.indexfact import IndexFactSerializer


class IndexFactListCreateAPIView(ListAPIView):
    """
    required in request body:
     - contour = id of contour
     - index = id of index
     - date = date of satellite images that have to proces
    """

    def get(self, request, *args, **kwargs):
        response = IndexFact.objects.filter(
            contour=request.data['contour']
        ).filter(
            index=request.data['index']
        ).filter(
            date=request.data['date']
        )

        if len(response) <= 0:
            index = Index.objects.get(id=request.data['index'])
            contour = Contour.objects.get(id=request.data['contour'])
            index_fact = IndexFact.objects.create(contour=contour, index=index, date=request.data['date'])
            index_fact.save()
        response = IndexFact.objects.filter(
            contour=request.data['contour']
        ).filter(index=request.data['index']
                 ).filter(
            date=request.data['date']
        )
        serializer = IndexFactSerializer(response, many=True)
        return Response(serializer.data, status=200)
