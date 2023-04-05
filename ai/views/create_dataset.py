from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from ai.utils.predicted_contour import create_rgb, cut_rgb_tif, merge_bands, deleted_files
from ai.utils.create_dataset import create_dataset


class CreateAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        merge_bands()
        create_rgb()
        cut_rgb_tif()
        create_dataset()
        deleted_files()
        return Response({"message": "ok"})
