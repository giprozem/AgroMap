from django.contrib.gis.geos import Polygon
from rest_framework.response import Response
from rest_framework.views import APIView
from ai.utils.predicted_contour import create_rgb, cut_rgb_tif, merge_bands, deleted_files, yolo, create_dataset
from rest_framework import viewsets
from ai.serializers import Contour_AISerializer
from ai.models.predicted_contour import Contour_AI
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import connection
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


class CutAPIView(APIView):
    def get(self, request):
        # merge_bands()
        # create_rgb()
        # cut_rgb_tif()
        yolo()
        # deleted_files()
        return Response({"message": "ok"})


class CreateAPIView(APIView):
    # permission_classes = (IsAdminUser,)

    def get(self, request):
        #merge_bands()
        #create_rgb()
        #cut_rgb_tif()
        create_dataset()
        # deleted_files()
        return Response({"message": "ok"})


class Contour_AIViewSet(viewsets.ModelViewSet):
    queryset = Contour_AI.objects.all()
    serializer_class = Contour_AISerializer
    # permission_classes = (IsAuthenticated,)


class Contour_AIInScreen(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                '_southWest': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'lat': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'lng': openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                    required=['lat', 'lng']
                ),
                '_northEast': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'lat': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'lng': openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                    required=['lat', 'lng']
                ),
            },
            required=['_southWest', '_northEast']
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'type': openapi.Schema(type=openapi.TYPE_STRING),
                    'features': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'type': openapi.Schema(type=openapi.TYPE_STRING),
                                'properties': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'contour_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'contour_ink': openapi.Schema(type=openapi.TYPE_STRING),
                                        'conton_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'farmer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'contour_year_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'productivity': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'land_type': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    }
                                ),
                                'geometry': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'type': openapi.Schema(type=openapi.TYPE_STRING),
                                        'coordinates': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(
                                                    type=openapi.TYPE_ARRAY,
                                                    items=openapi.Schema(
                                                        type=openapi.TYPE_NUMBER,
                                                    ),
                                                ),
                                            ),
                                        ),
                                    },
                                ),
                            },
                        ),
                    ),
                },
            ),
        },
        operation_description="Your operation description goes here",
    )
    def post(self, request, *args, **kwargs):
        """
        *Example*
            {
            "_southWest": {
                "lat": 42.70399473713915,
                "lng": 78.38859908922761
            },
            "_northEast": {
                "lat": 42.71093250783867,
                "lng": 78.4042846475467
            }
            }
        """

        if request.data:
            bboxs = Polygon.from_bbox((request.data['_southWest']['lng'], request.data['_southWest']['lat'],
                                       request.data['_northEast']['lng'], request.data['_northEast']['lat']))

            with connection.cursor() as cursor:
                cursor.execute(f"""
                               SELECT id, conton_id, district_id, culture,
                               St_AsGeoJSON(cntr.polygon) AS polygon
                               FROM ai_contour_ai AS cntr
                               WHERE ST_Intersects('{bboxs}'::geography::geometry, cntr.polygon::geometry);
                               """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature",
                                 "properties": {'id': i[0], 'conton_id': i[1],  'district_id': i[2], 'culture': i[3]},
                                 "geometry": eval(i[4])})
                return Response({"type": "FeatureCollection", "features": data})
        else:
            return Response(data={"message": "parameter is required"}, status=400)
