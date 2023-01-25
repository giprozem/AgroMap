from django.contrib.gis.geos import Point, Polygon
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView


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
            with connection.cursor() as cursor:
                cursor.execute(f"""
                               select cntr.id as contour_id, cntr.ink as ink, St_AsGeoJSON(cntr.polygon) as polygon
                               from gip_contour as cntr 
                               where ST_Contains('{bboxs}'::geography::geometry, cntr.polygon::geometry);
                               """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature",
                                 "properties": {'contour_id': i[0], 'ink': i[1]},
                                 "geometry": eval(i[2])})
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
                                 "properties": {'year': i[1], 'contour_id': i[0], 'ink': i[2], 'crop_yield': i[-1], 'culture_name': i[3]},
                                 "geometry": eval(i[4])})
                return Response({"type": "FeatureCollection", "features": data})
        else:
            return Response(data={"message": "parameter 'bbox or polygon_properties' is required"}, status=400)

