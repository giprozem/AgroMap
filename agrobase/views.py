from rest_framework import viewsets

from agrobase.models import Material
from agrobase.serializers import MaterialSerializer


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
