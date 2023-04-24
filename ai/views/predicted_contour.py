from django.contrib.gis.geos import Polygon
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets
from ai.serializers import Contour_AISerializer, UpdateContour_AISerializer
from ai.models.predicted_contour import Contour_AI
from ai.models.create_dataset import AI_Found, Process
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db import connection
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from notifications.signals import notify
from ai.utils.predicted_contour import deleted_files


class SearchAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        process = Process.objects.get(id=1)
        if process.is_running:
            message = "Процесс сейчас идёт"
        else:
            user = request.user
            Process.objects.all().delete()
            Process.objects.create(is_running=True, type_of_process=1)
            @receiver(post_save, sender=AI_Found)
            def my_handler(sender, instance, created, **kwargs):
                if created:
                    notify.send(instance, recipient=user, verb='Поиск контуров завершен')
                    deleted_files()
            message = "Процесс запущен"
        return Response({"message": message})


class Contour_AIViewSet(viewsets.ModelViewSet):
    queryset = Contour_AI.objects.all().order_by('id').filter(is_deleted=False)
    serializer_class = Contour_AISerializer

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'get':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UpdateContour_AISerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response('Contour is deleted')


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
                               SELECT cntr.id, conton_id, district_id, is_deleted, area_ha, elevation,
                               productivity, type_id, year, clt.id, clt.name_ru, clt.name_ky, clt.name_en, 
                               St_AsGeoJSON(cntr.polygon) AS polygon
                               FROM ai_contour_ai AS cntr
                               left JOIN gip_culture AS clt ON clt.id=cntr.culture_id
                               WHERE ST_Intersects('{bboxs}'::geography::geometry, cntr.polygon::geometry)
                               and cntr.is_deleted=false and cntr.id > 11016;
                               """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature",
                                 "properties": {'id': i[0], 'conton_id': i[1],  'district_id': i[2],
                                                'is_deleted': i[3], 'area_ha': i[4], 'elevation': i[5],
                                                'productivity': i[6], 'land_type': i[7], 'year': i[8],
                                                'culture': {'id': i[9], 'name_ru': i[10], 'name_ky': i[11], 'name_en': i[12]}
                                                },
                                 "geometry": eval(i[-1])})
                return Response({"type": "FeatureCollection", "features": data})
        else:
            return Response(data={"message": "parameter is required"}, status=400)
