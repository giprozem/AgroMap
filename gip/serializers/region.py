from rest_framework_gis.serializers import GeoFeatureModelSerializer

from gip.models import Region


class RegionSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Region
        exclude = ('name',)
        geo_field = 'polygon'

