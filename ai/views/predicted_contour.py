from rest_framework.response import Response
from rest_framework.views import APIView
from ai.utils.predicted_contour import create_rgb, cut_rgb_tif, merge_bands, deleted_files, yolo


class CutAPIView(APIView):
    def get(self, request):
        merge_bands()
        create_rgb()
        cut_rgb_tif()
        # deleted_files()
        yolo()
        return Response({"message": "ok"})

