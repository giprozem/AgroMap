from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from gip.models.conton import Conton
from gip.models.contour import Contour


class ContonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conton
        fields = ('polygon', )


class ContourSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Contour
        fields = '__all__'
        geo_field = 'polygon'


class ContourAutocompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = ('polygon', )


class CalculatePolygonContourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = '__all__'