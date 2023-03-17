from rest_framework import serializers
from gip.models import Conton, Region


class ContonSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField()

    def get_region(self, obj):
        region = Region.objects.get(name=obj.district.region)
        return region.pk

    class Meta:
        model = Conton
        exclude = ('name', )


class ContonWithoutPolygonSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField()

    def get_region(self, obj):
        region = Region.objects.get(name=obj.district.region)
        return region.pk

    class Meta:
        model = Conton
        exclude = ('polygon', 'name', 'created_at', 'updated_at',)
