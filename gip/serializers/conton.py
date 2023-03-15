from rest_framework import serializers
from gip.models import Conton, Region, District
from gip.serializers.region import RegionWithoutPolygonSerializer


class ContonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conton
        exclude = ('name', )


class DistrictWithoutPolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        exclude = ('polygon', 'created_at', 'updated_at', 'name', 'region')


class ContonWithoutPolygonSerializer(serializers.ModelSerializer):
    polygon = serializers.NullBooleanField(default=False)
    district = DistrictWithoutPolygonSerializer()
    region = serializers.SerializerMethodField()

    class Meta:
        model = Conton
        exclude = ('polygon', 'name', 'created_at', 'updated_at',)

    def get_region(self, obj):
        return RegionWithoutPolygonSerializer(Region.objects.get(name=obj.district.region)).data
