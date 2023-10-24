from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


def get_shapefile_upload_schema() -> swagger_auto_schema:
    return swagger_auto_schema(
        operation_description="Upload and extract shapefiles from a zip/rar file.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["file"],
            properties={
                "file": openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description="Zip/Rar file containing shapefiles.",
                )
            },
        ),
    )


def get_shapefile_export_schema() -> swagger_auto_schema:
    return swagger_auto_schema(
        operation_description="Export and zip shapefiles for a specified contour.",
        manual_parameters=[
            openapi.Parameter(
                "contour_id",
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="ID of the contour to export.",
            )
        ],
    )
