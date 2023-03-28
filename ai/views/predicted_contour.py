from rest_framework.response import Response
from rest_framework.views import APIView
from ai.utils import cut_image, create_rgb


class CutAPIView(APIView):
    def post(self, request):
        create_rgb()
        # cut_image()
        return Response({"message": "ok"})
