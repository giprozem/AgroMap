from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from gip.models import CropYield
from gip.models.conton import Conton
from gip.models.contour import Contour


class ContonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conton
        fields = ('polygon', )


class ContoursSerializer(GeoFeatureModelSerializer):
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


class CropYieldInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropYield
        fields = ('id', 'year', 'culture')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['culture'] = instance.culture.name
        return representation


class ContourSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Contour
        fields = '__all__'
        geo_field = 'polygon'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['properties'] = {'created_at': instance.created_at, 'updated_at': instance.updated_at,
                                        'ink': instance.ink, 'sum_ha': instance.sum_ha, 'conton': instance.conton.name,
                                        'farmer': instance.farmer.pin_inn,
                                        'culture': instance.crop_yields.order_by("-year").first().culture.name,
                                        'crop_yield': instance.sum_ha * instance.crop_yields.order_by("-year").first().culture.coefficient_crop,
                                        }

        return representation
