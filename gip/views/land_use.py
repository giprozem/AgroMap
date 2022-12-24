from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from gip.models import Contour
from gip.serializers.land_use import LandUseSerializer


class LandUseViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all()[320:]
    serializer_class = LandUseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ink', 'conton']
