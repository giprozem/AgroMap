from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from gip.models.culture import Culture
from gip.serializers.culture import CultureSerializer


class CultureViewSet(ModelViewSet):
    queryset = Culture.objects.all()
    serializer_class = CultureSerializer
    # permission_classes = (IsAuthenticated,)
