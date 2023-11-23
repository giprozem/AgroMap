from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


from django.http import HttpResponse

from gip.forms import ShapeFileUploadForm, ShapeFileExportAllData
from gip.models.contour import Contour
from gip.services.shapefile import UploadAndExtractService, ExportAndZipService
from gip.schemas.shapefile import (
    get_shapefile_export_schema,
    get_shapefile_upload_schema,
)


class UploadShapefileApiView(APIView):
    @get_shapefile_upload_schema()
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
    @get_shapefile_export_schema()
    def get(self, request, *args, **kwargs):
        contour_id = self.request.query_params.get("contour_id")

        if contour_id is None:
            return Response(data={"contour_id is required query param"})
        export_service = ExportAndZipService(model=Contour)
        file_content = export_service.execute(pk=contour_id)
        response = HttpResponse(file_content, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=agro-map.zip"
        return response


def import_shapefile(request):
    if request.method == "POST":
        form = ShapeFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            messages.success(request, _("Shapefile loaded successfully."))
            return redirect("admin:gip_contour_changelist")
        else:
            messages.error(request, _("Not valid shapefile"))
            messages.info(request, _("Make sure the shapefile is formed correctly"))
            return redirect("admin:gip_contour_changelist")

    return redirect("admin:gip_contour_changelist")


def export_all_data_shapefile(request):
    service = ExportAndZipService(model=Contour)
    file_content = service.execute()
    response = HttpResponse(file_content, content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=agro-map.zip"
    messages.success(request, _("Please wait while the file downloads"))
    return response
