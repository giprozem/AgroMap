from rest_framework import viewsets

from gip.models import ContourYear
from indexes.serializers.statistics_veg_index import ContourYearStatisticsSerializer


class ContourYearViewSet(viewsets.ModelViewSet):
    queryset = ContourYear.objects.all()
    serializer_class = ContourYearStatisticsSerializer
