from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from hub.models import LandInfo
from hub.serializers.land_info import LandInfoSerializers, LandInfoCustomSearchSerializer


class LandInfoViewSet(viewsets.ModelViewSet):
    queryset = LandInfo.objects.all()
    serializer_class = LandInfoSerializers
    lookup_field = 'ink_code'


class LandInfoSearch(APIView):
    def get(self, request, *args, **kwargs):
        search = request.GET.get('search', '')
        land_info = LandInfo.objects.all()
        if search:
            ink_code = land_info.filter(ink_code__icontains=search)
            return Response({"list_ink_code": LandInfoCustomSearchSerializer(ink_code, many=True).data})
