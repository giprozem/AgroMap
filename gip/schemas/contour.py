from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status


def get_filter_contour_shema() -> swagger_auto_schema:
    return swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "year", openapi.IN_QUERY, description="Year", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "land_type",
                openapi.IN_QUERY,
                description="Land type",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "region",
                openapi.IN_QUERY,
                description="Region",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "district",
                openapi.IN_QUERY,
                description="District",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "conton",
                openapi.IN_QUERY,
                description="Conton",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "culture",
                openapi.IN_QUERY,
                description="Culture",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "ai", openapi.IN_QUERY, description="AI", type=openapi.TYPE_BOOLEAN
            ),
        ],
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
    )


def get_statistic_contour_peoductivity_schema() -> swagger_auto_schema:
    return swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "year", openapi.IN_QUERY, description="Year", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "land_type",
                openapi.IN_QUERY,
                description="Land type",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "region",
                openapi.IN_QUERY,
                description="Region",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "district",
                openapi.IN_QUERY,
                description="District",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "conton",
                openapi.IN_QUERY,
                description="Conton",
                type=openapi.TYPE_INTEGER,
            ),
        ],
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
    )


def get_map_contour_productivitu_schema() -> swagger_auto_schema:
    return swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "year", openapi.IN_QUERY, description="Year", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "land_type",
                openapi.IN_QUERY,
                description="Land type",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "region",
                openapi.IN_QUERY,
                description="Region",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "district",
                openapi.IN_QUERY,
                description="District",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "conton",
                openapi.IN_QUERY,
                description="Conton",
                type=openapi.TYPE_INTEGER,
            ),
        ],
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
    )


def get_culture_statistics_schema() -> swagger_auto_schema:
    return swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "year", openapi.IN_QUERY, description="Year", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "land_type",
                openapi.IN_QUERY,
                description="Land type",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "region",
                openapi.IN_QUERY,
                description="Region",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "district",
                openapi.IN_QUERY,
                description="District",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "conton",
                openapi.IN_QUERY,
                description="Conton",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "culture",
                openapi.IN_QUERY,
                description="Culture",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "ai", openapi.IN_QUERY, description="AI", type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "culture_name_ru": openapi.Schema(type=openapi.TYPE_STRING),
                    "culture_name_ky": openapi.Schema(type=openapi.TYPE_STRING),
                    "culture_name_en": openapi.Schema(type=openapi.TYPE_STRING),
                    "area_ha": openapi.Schema(type=openapi.TYPE_NUMBER),
                    "productivity": openapi.Schema(type=openapi.TYPE_NUMBER),
                    "territory_ru": openapi.Schema(type=openapi.TYPE_STRING),
                    "territory_ky": openapi.Schema(type=openapi.TYPE_STRING),
                    "territory_en": openapi.Schema(type=openapi.TYPE_STRING),
                },
            )
        },
    )
