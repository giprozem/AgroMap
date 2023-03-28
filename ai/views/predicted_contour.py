from rest_framework.response import Response
from rest_framework.views import APIView
from ai.utils import create_rgb, cut_image


class CutAPIView(APIView):
    def post(self, request):
        create_rgb()
        cut_image()
        return Response({"message": "ok"})
