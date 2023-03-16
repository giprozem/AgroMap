from django.contrib.gis.geos import Point, Polygon
from django.db import connection
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import Contour


class OccurrenceCheckAPIView(APIView):
    def get(self, request, *args, **kwargs):
        point = request.GET.get('point')
        polygon = request.GET.get('polygon')

        if point:
            points = Point(eval(point))
            with connection.cursor() as cursor:
                cursor.execute(f"""
                               select rgn.name as region_name,  dst.name as district_name, cntn.name as conton_name 
                               from gip_district as dst join gip_region as rgn
                               on rgn.id = dst.region_id
                               join gip_conton as cntn
                               on dst.id = cntn.district_id 
                               where ST_Contains(cntn.polygon::geometry, '{points}'::geography::geometry);
                               """)
                rows = cursor.fetchall()
                data = {
                    'region': f"{[row[0] for row in rows]}".strip("['']"),
                    'district': f"{[row[1] for row in rows]}".strip("['']"),
                    'conton': f"{[row[-1] for row in rows]}".strip("['']")
                }
                return Response(data)
        elif polygon:
            polygons = Polygon(eval(polygon))
            with connection.cursor() as cursor:
                cursor.execute(f"""
                               select rgn.name as region_name,  dst.name as district_name, cntn.name as conton_name 
                               from gip_district as dst join gip_region as rgn
                               on rgn.id = dst.region_id
                               join gip_conton as cntn
                               on dst.id = cntn.district_id 
                               where ST_Contains(cntn.polygon::geometry, '{polygons}'::geography::geometry);
                               """)
                rows = cursor.fetchall()
                data = {
                    'region': f"{[row[0] for row in rows]}".strip("['']"),
                    'district': f"{[row[1] for row in rows]}".strip("['']"),
                    'conton': f"{[row[-1] for row in rows]}".strip("['']")
                }
                return Response(data)
        else:
            return Response(data={"message": "parameter 'point or polygon' is required"}, status=400)


class PolygonsInBbox(APIView):
    def get(self, request, *args, **kwargs):
        bbox = request.GET.get('bbox')
        polygon_properties = request.GET.get('polygon_properties')

        if bbox:
            bboxs = Polygon(eval(bbox))
            print(bboxs)
            with connection.cursor() as cursor:
                cursor.execute(f"""
                               SELECT cntr.id, cntr.ink, cntr.conton_id, cntr.farmer_id, gcy.id,
                               gcy.code_soato, gcy.year, gcy.productivity, gcy.type_id,
                               St_AsGeoJSON(gcy.polygon) AS polygon
                               FROM  gip_contour AS cntr
                               INNER JOIN gip_contouryear_contour AS cyc ON cntr.id=cyc.contour_id
                               INNER JOIN gip_contouryear AS gcy ON gcy.id=cyc.contouryear_id
                               where ST_Intersects('{bboxs}'::geography::geometry, gcy.polygon::geometry);
                               """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature",
                                 "properties": {'contour_id': i[0],'contour_ink': i[1],'conton_id': i[2],'farmer_id': i[3],
                                                'contour_year_id': i[4], 'productivity': i[5], 'land_type': i[6]},
                                 "geometry": eval(i[-1])})
                return Response({"type": "FeatureCollection", "features": data})
        elif polygon_properties:
            bbox_properties = Polygon(eval(polygon_properties))
            with connection.cursor() as cursor:
                cursor.execute(f"""
                               select distinct on (cntr.id) cntr.id, cy.year as year, cntr.ink, cl.name, St_AsGeoJSON(cntr.polygon) as polygon,
                               round(sum(cntr.area_ha * cl.coefficient_crop)::numeric, 2) as sum
                               from gip_contour as cntr
                               join gip_cropyield as cy
                               on cntr.id = cy.contour_id
                               join gip_culture as cl
                               on cl.id = cy.culture_id
                               where ST_Contains('{bbox_properties}'::geography::geometry, cntr.polygon::geometry)
                               group by cntr.id, cntr.ink, cl.name, cy.year
                               order by cntr.id, cy.year desc;
                               """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature",
                                 "properties": {'year': i[1], 'contour_id': i[0], 'ink': i[2], 'crop_yield': i[-1],
                                                'culture_name': i[3]},
                                 "geometry": eval(i[4])})
                return Response({"type": "FeatureCollection", "features": data})
        else:
            return Response(data={"message": "parameter 'bbox or polygon_properties' is required"}, status=400)


class PolygonsInScreen(APIView):

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
                               SELECT id, conton_id, farmer_id, ink, is_rounded, code_soato, is_deleted, area_ha,
                               culture_id, elevation, productivity, type_id, year,
                               St_AsGeoJSON(cntr.polygon) AS polygon
                               FROM gip_contour AS cntr
                               WHERE ST_Intersects('{bboxs}'::geography::geometry, cntr.polygon::geometry);
                               """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature",
                                 "properties": {'id': i[0], 'conton_id': i[1],  'farmer_id': i[2], 'ink': i[3],
                                                'is_rounded': i[4], 'code_soato': i[5], 'is_deleted': i[6],
                                                'area_ha': i[7], 'culture_id': i[8], 'elevation': i[9],
                                                'productivity': i[10], 'land_type': i[11], 'year': i[12]},
                                 "geometry": eval(i[13])})
                return Response({"type": "FeatureCollection", "features": data})
        else:
            return Response(data={"message": "parameter is required"}, status=400)
