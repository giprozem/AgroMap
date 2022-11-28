from rest_framework import viewsets

from gip.models import Culture
from gip.serializers.culture import CultureSerializer


class CultureViewSet(viewsets.ModelViewSet):
    queryset = Culture.objects.all()
    serializer_class = CultureSerializer