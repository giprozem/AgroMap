from rest_framework import viewsets

from gip.models import District
from gip.serializers.district import DistrictSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer