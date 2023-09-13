from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from django.http import FileResponse, HttpResponse

from gip.models.contour import Contour
from gip.services.shapefile import UploadAndExtractService, ExportAndZipService


class UploadShapefileApiView(APIView):
    def post(self, request, *args, **kwargs):
        file = self.request.FILES.get("file")
        if file is None:
            return Response(data={"message": "file is required"})
        else:
            if file.name.endswith(".zip") or file.name.endswith(".rar"):
                upload_service = UploadAndExtractService(zip_file=file, model=Contour)
                upload_service.execute()
                return Response("Shapefile upload successfully")


class ExportShapefileApiView(APIView):
    def get(self, request, *args, **kwargs):
        contour_id = self.request.query_params.get("contour_id")
        if contour_id is None:
            return Response(data={"contour_id is required query param"})
        export_service = ExportAndZipService(model=Contour)
        file_content = export_service.execute(pk=contour_id)
        response = HttpResponse(file_content, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=hui.zip'
        return response
