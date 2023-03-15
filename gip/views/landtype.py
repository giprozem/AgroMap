from rest_framework.generics import ListAPIView
from gip.models.contour import LandType
from gip.serializers.landtype import LandTypeSerializer
from rest_framework.permissions import IsAuthenticated


class LandTypeAPIView(ListAPIView):
    queryset = LandType.objects.all()
    serializer_class = LandTypeSerializer
    permission_classes = (IsAuthenticated,)
