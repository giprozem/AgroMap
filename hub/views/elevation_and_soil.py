from django.db import connection
from elevation.data import elevation
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView


class ElevationSoilAPIView(APIView):
    def get(self, request, *args, **kwargs):
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        try:
            if latitude and longitude:
                with connection.cursor() as cursor:
                    cursor.execute(f""" SELECT sc.id_soil, sc.name, scm.id FROM gip_soilclassmap AS scm
                                        JOIN gip_soilclass AS sc ON sc.id = scm.soil_class_id
                                        WHERE ST_CONTAINS(scm.polygon::geometry, 
                                        'Point({longitude} {latitude})'::geography::geometry) = true;
                                    """)
                    rows = cursor.fetchall()
                    return Response({
                        'soil': rows[0][1] if rows != [] else None,
                        'elevation': elevation(latitude=float(latitude), longitude=float(longitude))
                    })
            else:
                return Response(data={"message": "parameter 'latitude and longitude' is required"}, status=400)
        except Exception as e:
            raise APIException({
                "message": e
            })
