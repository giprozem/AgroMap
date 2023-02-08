from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from gip.models import District
from gip.serializers.district import DistrictSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['region', ]