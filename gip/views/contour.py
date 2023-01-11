from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from gip.models.contour import Contour
from gip.serializers.contour import ContoursSerializer, ContourSerializer


class ContoursViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all()
    serializer_class = ContoursSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ink', 'conton']


class ContourViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ink', 'conton']
    # pagination_class = ContourPagination
