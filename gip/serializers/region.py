from rest_framework_gis.serializers import GeoFeatureModelSerializer

from gip.models import Region


class RegionSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        geo_field = 'polygon'

