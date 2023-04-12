from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from gip.models.culture import Culture
from gip.serializers.culture import CultureSerializer


class CultureViewSet(ModelViewSet):
    queryset = Culture.objects.all()
    serializer_class = CultureSerializer

    # def get_permissions(self):
    #     if self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]
