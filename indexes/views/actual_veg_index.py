from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from indexes.models.actual_veg_index import ActualVegIndex
from indexes.serializers.actual_veg_index import ActuaVegIndexSerializer


class ActualIndexesOfContourYear(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='contour_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Contour ID',
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description='Successful response',
                schema=ActuaVegIndexSerializer(many=True)
            ),
            400: openapi.Response(
                description='We have no data to show',
                schema=ActuaVegIndexSerializer(many=True)
            )
        },
        operation_summary='required contour_id return all indexes and values of required conrour'
    )
    def get(self, request, *args, **kwargs):

        response = ActualVegIndex.objects.filter(contour=request.query_params['contour_id'])
        serializer = ActuaVegIndexSerializer(response, many=True, context={'request': request})
        if response:
            return Response(serializer.data, status=200)
        return Response([], status=200)


class SatelliteImagesDate(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description='Successful response',
                schema=ActuaVegIndexSerializer(many=True)
            ),
            400: openapi.Response(
                description='We have no data to show',
                schema=ActuaVegIndexSerializer(many=True)
            )
        },
        operation_summary='required contour_id return all indexes and values of required conrour'
    )
    def get(self, request, *args, **kwargs):
        index = kwargs['index']
        contour = kwargs['contour']
        result = ActualVegIndex.objects.filter(index=index).filter(contour=contour)
        serializer = ActuaVegIndexSerializer(result, many=True)
        return Response(serializer.data, status=200)

