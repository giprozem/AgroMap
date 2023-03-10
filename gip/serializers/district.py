from rest_framework_gis import serializers

from gip.models import District


class DistrictSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = District
        exclude = ('name',)
        geo_field = 'polygon'


class DistrictWithoutPolygonSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        exclude = ('polygon', 'created_at', 'updated_at', 'name', )
