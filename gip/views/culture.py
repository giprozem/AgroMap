from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from gip.models.culture import Culture
from gip.serializers.culture import CultureSerializer


class CultureViewSet(ModelViewSet):
    queryset = Culture.objects.all()
    serializer_class = CultureSerializer

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
