from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from gip.models import Contour
from gip.serializers.contour import ContourSerializer


class LandUseSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Contour
        fields = '__all__'
        geo_field = 'polygon'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['properties'] = {'created_at': instance.created_at, 'updated_at': instance.updated_at,
                                        'ink': instance.ink, 'sum_ha': instance.sum_ha, 'conton': instance.conton.name,
                                        'farmer': instance.farmer.pin_inn,
                                        }

        if instance.crop_yields.exists():
            culture = instance.crop_yields.order_by("-year").first().culture
            representation['properties']["culture"] = culture.name
            representation['properties']['crop_yield'] = round(culture.coefficient_crop * instance.sum_ha, 2)
            representation['properties']['group'] = culture.name
        else:
            representation['properties']['group'] = "Неиспользуемые земли"

        return representation
