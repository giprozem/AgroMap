from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status


def get_polygon_in_screen_schema() -> swagger_auto_schema:
    return swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "land_type",
                openapi.IN_QUERY,
                description="Land type",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "culture",
                openapi.IN_QUERY,
                description="Culture",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "year", openapi.IN_QUERY, description="Year", type=openapi.TYPE_INTEGER
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "_southWest": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "lat": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "lng": openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                    required=["lat", "lng"],
                ),
                "_northEast": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "lat": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "lng": openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                    required=["lat", "lng"],
                ),
            },
            required=["_southWest", "_northEast"],
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "type": openapi.Schema(type=openapi.TYPE_STRING),
                    "features": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "type": openapi.Schema(type=openapi.TYPE_STRING),
                                "properties": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "contour_id": openapi.Schema(
                                            type=openapi.TYPE_INTEGER
                                        ),
                                        "contour_ink": openapi.Schema(
                                            type=openapi.TYPE_STRING
                                        ),
                                        "conton_id": openapi.Schema(
                                            type=openapi.TYPE_INTEGER
                                        ),
                                        "farmer_id": openapi.Schema(
                                            type=openapi.TYPE_INTEGER
                                        ),
                                        "contour_year_id": openapi.Schema(
                                            type=openapi.TYPE_INTEGER
                                        ),
                                        "productivity": openapi.Schema(
                                            type=openapi.TYPE_INTEGER
                                        ),
                                        "land_type": openapi.Schema(
                                            type=openapi.TYPE_INTEGER
                                        ),
                                    },
                                ),
                                "geometry": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "type": openapi.Schema(
                                            type=openapi.TYPE_STRING
                                        ),
                                        "coordinates": openapi.Schema(
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
