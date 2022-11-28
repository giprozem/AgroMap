from rest_framework import viewsets

from gip.models import Conton
from gip.serializers.conton import ContonSerializer


class ContonViewSet(viewsets.ModelViewSet):
    queryset = Conton.objects.all()
    serializer_class = ContonSerializer