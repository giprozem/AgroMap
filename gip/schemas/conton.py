from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


def get_conton_schema() -> swagger_auto_schema:
    return swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "page_size",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Page_size is optional",
            ),
            openapi.Parameter(
                "polygon",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="If set, returns the serialized polygon for each district. "
                "If doesnot set, returns only the district data without polygons.",
            ),
            openapi.Parameter(
                "district_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="If `polygon` is set, this parameter can be used to filter districts by district ID.",
            ),
            openapi.Parameter(
                "pagination",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="If set, returns the serialized data with pagination. "
                "If doesnot set, returns only the district data without pagination.",
            ),
        ],
        responses={
            200: openapi.Response(
                "OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "name": openapi.Schema(type=openapi.TYPE_STRING),
                            "district_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "polygon": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "type": openapi.Schema(
                                        type=openapi.TYPE_STRING, example="Polygon"
                                    ),
                                    "coordinates": openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(
                                                    type=openapi.TYPE_NUMBER
                                                ),
                                            ),
                                        ),
                                    ),
                                },
                            ),
                        },
                    ),
                ),
            ),
            400: openapi.Response("Bad Request"),
        },
    )
