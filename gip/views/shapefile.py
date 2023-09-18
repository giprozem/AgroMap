from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from django.http import FileResponse, HttpResponse

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from gip.models.contour import Contour
from gip.services.shapefile import UploadAndExtractService, ExportAndZipService


class UploadShapefileApiView(APIView):
    @swagger_auto_schema(
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
        )
    )
    def post(self, request, *args, **kwargs):
        file = self.request.FILES.get("file")
        if file is None:
            return Response(data={"message": "file is required"})

        if file.name.endswith(".zip") or file.name.endswith(".rar"):
            upload_service = UploadAndExtractService(zip_file=file, model=Contour)
            upload_service.execute()
            return Response("Shapefile upload successfully", status=200)
        else:
            return Response(
                data={"message": "Unreadable file content, file must be rar or zip"},
                status=400,
            )


class ExportShapefileApiView(APIView):
    @swagger_auto_schema(
        operation_description="Export and zip shapefiles for a specified contour.",
        manual_parameters=[
            openapi.Parameter(
                "contour_id",
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="ID of the contour to export."
            )]
    )
    def get(self, request, *args, **kwargs):
        contour_id = self.request.query_params.get("contour_id")

        if contour_id is None:
            return Response(data={"contour_id is required query param"})
        export_service = ExportAndZipService(model=Contour)
        file_content = export_service.execute(pk=contour_id)
        response = HttpResponse(file_content, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=agro-map.zip"
        return response
