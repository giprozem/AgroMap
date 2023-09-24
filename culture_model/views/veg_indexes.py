# Import necessary modules and classes
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from culture_model.models.vegetation_index import VegetationIndex
from culture_model.serializers import IndexSerializer

# Create an API view class named VegIndexAPIView that inherits from APIView
class VegIndexAPIView(APIView):

    # Apply Swagger documentation to the 'get' method
    @swagger_auto_schema(
        operation_summary="Get all vegetation indexes",
        responses={
            200: IndexSerializer(many=True),  # Response for success with IndexSerializer
            400: "Have no vegetation indexes"  # Response for failure with an error message
        }
    )
    def get(self, request, *args, **kwargs):
        # Query the database to get all vegetation indexes and order them by 'id'
        query = VegetationIndex.objects.all().order_by('id')

        # Check if there are no vegetation indexes
        if len(query) <= 0:
            # Return a response with a 400 status code and an error message
            return Response('Have no vegetation indexes', status=400)

        # Serialize the query results using IndexSerializer
        serializer = IndexSerializer(query, many=True)

        # Return a response with a 200 status code and the serialized data
        return Response(serializer.data, status=200)
