from rest_framework import filters
from rest_framework import viewsets
from gip.serializers.contact_information import *


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['$name', ]


class ContactInformationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContactInformation.objects.all()
    serializer_class = ContactInformationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        region = self.request.query_params.get('region')
        district = self.request.query_params.get('district')
        if region and district:
            queryset = queryset.filter(district__region_id=region, district_id=district)
            return queryset
        return queryset
