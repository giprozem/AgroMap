from rest_framework import viewsets

from agrobase.models import Material, MaterialBlock, MaterialImage
from agrobase.serializers import MaterialSerializer, MaterialBlockSerializer, MaterialImageSerializer


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class MaterialBlockViewSet(viewsets.ModelViewSet):
    queryset = MaterialBlock.objects.all()
    serializer_class = MaterialBlockSerializer


class MaterialImageViewSet(viewsets.ModelViewSet):
    queryset = MaterialImage.objects.all()
    serializer_class = MaterialImageSerializer
