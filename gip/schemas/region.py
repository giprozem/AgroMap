from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status


def get_region_schema() -> swagger_auto_schema:
    return swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="polygon",
                in_=openapi.IN_QUERY,
                description="Flag to include/exclude polygon data",
                type=openapi.TYPE_BOOLEAN,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="List of regions",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(
                                type=openapi.TYPE_INTEGER, description="Region ID"
                            ),
                            "name": openapi.Schema(
                                type=openapi.TYPE_STRING, description="Region name"
                            ),
                            "polygon": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                description="Region polygon data",
                                properties={
                                    "type": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Polygon type",
                                    ),
                                    "coordinates": openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        description="List of coordinates",
                                        items=openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Schema(
                                                type=openapi.TYPE_NUMBER
                                            ),
                                        ),
                                    ),
                                },
                            ),
                        },
                    ),
                ),
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Error message"
                        )
                    },
                ),
            ),
        },
    )
