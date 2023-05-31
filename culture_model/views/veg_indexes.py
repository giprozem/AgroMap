from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from culture_model.models.vegetation_index import VegetationIndex
from culture_model.serializers import IndexSerializer


class VegIndexAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="Get all vegetation indexes",
        responses={
            200: IndexSerializer(many=True),
            400: "Have no vegetation indexes"
        }
    )
    def get(self, request, *args, **kwargs):
        query = VegetationIndex.objects.all().order_by('id')
        if len(query) <= 0:
            return Response('Have no vegetation indexes', status=400)
        serializer = IndexSerializer(query, many=True)
        return Response(serializer.data, status=200)
