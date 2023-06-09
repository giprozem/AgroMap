from rest_framework_gis import serializers

from gip.models import District
from gip.serializers.region import RegionWithoutPolygonSerializer


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        exclude = ('name',)


class DistrictWithoutPolygonSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        exclude = ('polygon', 'created_at', 'updated_at', 'name', )
