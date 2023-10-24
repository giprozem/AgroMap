from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from gip.serializers.soil import SoilClassSerializer


def get_soil_schema() -> swagger_auto_schema:
    return swagger_auto_schema(operation_summary="do not required for front")


def get_soil_class_schema() -> swagger_auto_schema:
    return swagger_auto_schema(
        operation_summary="Get all soil classes.",
        responses={200: SoilClassSerializer(many=True)},
    )
