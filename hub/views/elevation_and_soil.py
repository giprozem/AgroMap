# Importing necessary Django and DRF modules
from django.db import connection
from elevation.data import elevation
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

# ElevationSoilAPIView class definition. This APIView handles GET requests.
class ElevationSoilAPIView(APIView):

    # Define the GET method
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to fetch elevation and soil data for a given geographical point.
        
        Args:
            request (HttpRequest): Request object encapsulating the GET data.
        
        Returns:
            Response: JSON response containing elevation and soil data.
        """
        # Extract 'latitude' and 'longitude' parameters from the GET request
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        
        try:
            # Check if both latitude and longitude are provided
            if latitude and longitude:
                # Establish a connection to the database using Django's cursor
                with connection.cursor() as cursor:
                    # Execute the SQL query to fetch soil data based on the given geographical point
                    cursor.execute(f""" SELECT sc.id_soil, sc.name, scm.id FROM gip_soilclassmap AS scm
                                        JOIN gip_soilclass AS sc ON sc.id = scm.soil_class_id
                                        WHERE ST_CONTAINS(scm.polygon::geometry, 
                                        'Point({longitude} {latitude})'::geography::geometry) = true;
                                    """)
                    # Fetch all rows returned by the query
                    rows = cursor.fetchall()
                    # Return the response containing soil data (if available) and elevation data
                    return Response({
                        'soil': rows[0][1] if rows != [] else None,
                        'elevation': elevation(latitude=float(latitude), longitude=float(longitude))
                    })
            else:
                # If either latitude or longitude is missing, return an error response
                return Response(data={"message": "parameter 'latitude and longitude' is required"}, status=400)
        except Exception as e:
            # In case of any exception, raise an APIException with the error message
            raise APIException({
                "message": e
            })
