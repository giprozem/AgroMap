from rest_framework import viewsets

from gip.models import CropYield
from gip.serializers.crop_yield import CropYieldSerializer


class CropYieldViewSet(viewsets.ModelViewSet):
    queryset = CropYield.objects.all()
    serializer_class = CropYieldSerializer