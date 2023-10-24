from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from gip.models.soil import SoilClass
from rest_framework.response import Response
import json

from gip.serializers.soil import SoilClassSerializer
from gip.schemas.soil import get_soil_class_schema, get_soil_schema


class SoilAPIView(APIView):
    @get_soil_schema()
    def post(self, request, *args, **kwargs):
        with open("exel.json") as f:
            result = json.load(f)

        for i, j in result.items():
            SoilClass.objects.create(id_soil=i, name=j, name_ky=j, name_en=j)
        return Response("it is ok", status=200)


class SoilClassAPIView(APIView):
    @get_soil_class_schema()
    def get(self, request, *args, **kwargs):
        """
        Retrieve all soil classes.
        """
        query = SoilClass.objects.all().order_by("id_soil")
        serializer = SoilClassSerializer(query, many=True)
        return Response(serializer.data, status=200)
