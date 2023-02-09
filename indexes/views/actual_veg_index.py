from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from indexes.models.actual_veg_index import ActuaVegIndex
from indexes.serializers.actual_veg_index import ActuaVegIndexSerializer


class IndexFactListCreateAPIView(ListAPIView):
    """
    required in request params:
     - contour = id of contour
     - index = id of index
     - date = date of satellite images that have to proces
    """

    def get(self, request, *args, **kwargs):
        response = ActuaVegIndex.objects.filter(
            contour=request.query_params['contour']
        ).filter(
            index=request.query_params['index']
        ).filter(
            date=request.query_params['date']
        )

        serializer = ActuaVegIndexSerializer(response, many=True)
        return Response(serializer.data, status=200)


class SatelliteImagesDate(APIView):
    """
    required:
    first param = index_id
    second param = contour id
    """
    def get(self, request, *args, **kwargs):
        index = kwargs['index']
        contour = kwargs['contour']
        result = ActuaVegIndex.objects.filter(index=index).filter(contour=contour)
        serializer = ActuaVegIndexSerializer(result, many=True)
        return Response(serializer.data, status=200)


class ActualIndexesOfContourYear(APIView):
    """
    required:
    param = contour_id
    """

    def get(self, request, *args, **kwargs):
        contour = request.query_params['contour_id']
        response = ActuaVegIndex.objects.filter(contour=contour)
        serializer = ActuaVegIndexSerializer(response, many=True, context={'request': request})
        return Response(serializer.data, status=200)
