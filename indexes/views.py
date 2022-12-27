from rest_framework.viewsets import ModelViewSet

from indexes.models import NDVIIndex
from indexes.serializers import NDVISerializer, NDVIListSerializer


class NDVIViewSet(ModelViewSet):
    queryset = NDVIIndex.objects.all()
    serializer_class = NDVIListSerializer
    serializer_classes = {
        'create': NDVISerializer,
        'retrieve': NDVIListSerializer,
        'update': NDVISerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
