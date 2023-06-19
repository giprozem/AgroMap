from rest_framework_gis import serializers

from gip.models import District


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        exclude = ('name',)


class DistrictWithoutPolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        exclude = ('polygon', 'created_at', 'updated_at', 'name',)
