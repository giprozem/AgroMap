from rest_framework_gis import serializers

from gip.models import Region


class RegionSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = Region
        exclude = ('name',)
        geo_field = 'polygon'


class RegionWithoutPolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        exclude = ('polygon', 'name', 'created_at', 'updated_at', )
