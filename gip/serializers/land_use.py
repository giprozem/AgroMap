from rest_framework_gis.serializers import GeoFeatureModelSerializer

from gip.models import Contour


class LandUseSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Contour
        fields = '__all__'
        geo_field = 'polygon'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['properties'] = {'created_at': instance.created_at, 'updated_at': instance.updated_at,
                                        'ink': instance.ink, 'area_ha': instance.area_ha,
                                        'conton': instance.conton.name,
                                        'farmer': instance.farmer.pin_inn,
                                        }

        if instance.crop_yields.exists():
            culture = instance.crop_yields.order_by("-year").first().culture
            representation['properties']["culture"] = culture.name
            representation['properties']['crop_yield'] = round(culture.coefficient_crop * instance.area_ha, 2)
            representation['properties']['group'] = culture.name
            representation['properties']['fill_color'] = culture.fill_color
            representation['properties']['stroke_color'] = culture.stroke_color
        else:
            representation['properties']['group'] = "Unused land"
            representation['properties']['fill_color'] = "#3388FF"
            representation['properties']['stroke_color'] = "#3388FF"

        return representation
