from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from gip.models import CropYield
from gip.models.conton import Conton
from gip.models.contour import Contour, LandType, ContourYear


class ContonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conton
        fields = ('polygon', )


class ContourAutocompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = ('polygon', )


class CalculatePolygonContourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = '__all__'


class CropYieldInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropYield
        fields = ('id', 'year', 'culture')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['culture'] = instance.culture.name
        return representation


class ContourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = '__all__'


class ContourYearSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ContourYear
        exclude = ('productivity', )
        geo_field = 'polygon'


class LandTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandType
        exclude = ('name', )


class AuthDetailContourYearSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ContourYear
        exclude = ('productivity', )
        geo_field = 'polygon'


class AuthDetailContourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = '__all__'
