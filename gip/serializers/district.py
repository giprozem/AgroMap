from rest_framework_gis.serializers import GeoFeatureModelSerializer

from gip.models import District


class DistrictSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = District
        fields = '__all__'
        geo_field = 'polygon'

