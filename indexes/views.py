from rest_framework.viewsets import ModelViewSet

from indexes.models import NDVIIndex
from indexes.serializers import NDVISerializer


class NDVIViewSet(ModelViewSet):
    queryset = NDVIIndex.objects.all()
    serializer_class = NDVISerializer
