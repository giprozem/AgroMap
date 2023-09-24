from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from indexes.models.actual_veg_index import ActualVegIndex, PredictedContourVegIndex
from indexes.serializers.actual_veg_index import ActuaVegIndexSerializer, PredictedContourActuaVegIndexSerializer


class ActualIndexesOfContourYear(APIView):
    """
    API endpoint that retrieves all the vegetation indexes and their values for a given contour based on its ID.
    """

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
            204: openapi.Response(
                description='We have no data to show'
            )
        },
        operation_summary='required contour_id return all indexes and values of required contour'
    )
    def get(self, request, *args, **kwargs):
        # Queries the ActualVegIndex model with the given contour_id.
        response = ActualVegIndex.objects.filter(contour=request.query_params['contour_id']).order_by('date')
        # Serializes the response data.
        serializer = ActuaVegIndexSerializer(response, many=True, context={'request': request})
        # Returns the serialized data if it exists.
        if response:
            return Response(serializer.data, status=200)
        return Response([], status=204)


class SatelliteImagesDate(APIView):
    """
    API endpoint that retrieves all the vegetation indexes and their values for a given contour and index.
    """

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
        operation_summary='required contour_id return all indexes and values of required contour'
    )
    def get(self, request, *args, **kwargs):
        index = kwargs['index']
        contour = kwargs['contour']
        result = ActualVegIndex.objects.filter(index=index).filter(contour=contour).order_by('date')
        serializer = ActuaVegIndexSerializer(result, many=True)
        return Response(serializer.data, status=200)


class ActualIndexesOfContourAI(APIView):
    """
    API endpoint that retrieves all the vegetation indexes and their values for a given AI contour based on its ID.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='contourAI_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='ContourAI ID',
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description='Successful response',
                schema=PredictedContourActuaVegIndexSerializer(many=True)
            ),
            204: openapi.Response(
                description='We have no data to show'
            )
        },
        operation_summary='required contourAI_id return all indexes and values of required contour'
    )
    def get(self, request, *args, **kwargs):
        # Queries the PredictedContourVegIndex model with the given contourAI_id.
        response = PredictedContourVegIndex.objects.filter(contour=request.query_params['contour_id']).order_by('date')
        # Serializes the response data.
        serializer = PredictedContourActuaVegIndexSerializer(response, many=True, context={'request': request})
        # Returns the serialized data if it exists.
        if response:
            return Response(serializer.data, status=200)
        return Response([], status=204)


class PredictedSatelliteImagesDate(APIView):
    """
    API endpoint that retrieves all the predicted vegetation indexes and their values for a given AI contour and index.
    """

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description='Successful response',
                schema=PredictedContourActuaVegIndexSerializer(many=True)
            ),
            400: openapi.Response(
                description='We have no data to show'
            )
        },
        operation_summary='required contourAI_id return all indexes and values of required contour'
    )
    def get(self, request, *args, **kwargs):
        index = kwargs['index']
        contour = kwargs['contour']
        result = PredictedContourVegIndex.objects.filter(index=index).filter(contour=contour).order_by('date')
        serializer = PredictedContourActuaVegIndexSerializer(result, many=True)
        return Response(serializer.data, status=200)
