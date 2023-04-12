from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.models import Contour_AI
from indexes.models import SciHubImageDate
from indexes.models.actual_veg_index import ActualVegIndex, PredictedContourVegIndex
from indexes.serializers.actual_veg_index import ActuaVegIndexSerializer, PredictedContourActuaVegIndexSerializer


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
            204: openapi.Response(
                description='We have no data to show'
            )
        },
        operation_summary='required contour_id return all indexes and values of required contour'
    )
    def get(self, request, *args, **kwargs):

        response = ActualVegIndex.objects.filter(contour=request.query_params['contour_id']).order_by('date')
        serializer = ActuaVegIndexSerializer(response, many=True, context={'request': request})
        if response:
            return Response(serializer.data, status=200)
        return Response([], status=204)


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


class ActualIndexesOfContourAI(APIView):
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

        response = PredictedContourVegIndex.objects.filter(contour=request.query_params['contour_id']).order_by('date')
        serializer = PredictedContourActuaVegIndexSerializer(response, many=True, context={'request': request})
        if response:
            return Response(serializer.data, status=200)
        return Response([], status=204)


class PredictedSatelliteImagesDate(APIView):
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


class CleaningActualVegIndex(APIView):
    @swagger_auto_schema(
        operation_summary='do not required for front',
        description='clean all incorrect veg indexes'
    )
    def post(self, request, *args, **kwargs):
        image_dates = SciHubImageDate.objects.all()
        for j in range(1, (PredictedContourVegIndex.objects.all().last().id + 1)):
            for i in image_dates:
                image_date = i.date
                image_date = image_date.strftime('%Y-%m-%d')
                veg = PredictedContourVegIndex.objects.filter(contour_id=j, date=image_date, average_value=0)
                if len(veg) == 6:
                    for c in veg:
                        PredictedContourVegIndex.objects.filter(id=c.id).delete()
        return Response('all deleted', status=200)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='satellite_image_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='satellite_image_id',
                required=True
            )
        ],
        operation_summary='do not required for front',
        description='clean all incorrect veg indexes in one satellite image'
    )
    def get(self, request, *args, **kwargs):
        satellite_image_id = request.query_params['satellite_image_id']
        satellite_image = SciHubImageDate.objects.filter(id=satellite_image_id)
        contours = Contour_AI.objects.filter(polygon__coveredby=satellite_image[0].polygon)
        image_date = satellite_image[0].date
        image_date = image_date.strftime('%Y-%m-%d')
        for contour in contours:
            veg = PredictedContourVegIndex.objects.filter(contour_id=contour, date=image_date, average_value=0)
            if len(veg) == 6:
                for c in veg:
                    PredictedContourVegIndex.objects.filter(id=c.id).delete()
        return Response('successfully', status=200)
