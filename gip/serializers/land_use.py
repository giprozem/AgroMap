# Import the GeoFeatureModelSerializer from rest_framework_gis.serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

# Import the Contour model from the 'gip' application
from gip.models import Contour

# Define a serializer for representing land use, inheriting from GeoFeatureModelSerializer
class LandUseSerializer(GeoFeatureModelSerializer):
    class Meta:
        # Specify the model that this serializer is associated with
        model = Contour

        # Include all fields from the model in the serialized representation
        fields = '__all__'

        # Specify the geometry field (the field representing the polygon)
        geo_field = 'polygon'

    def to_representation(self, instance):
        # Call the parent class's to_representation method
        representation = super().to_representation(instance)

        # Add additional properties to the serialized representation
        representation['properties'] = {
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
            'ink': instance.ink,
            'area_ha': instance.area_ha,
            'conton': instance.conton.name,
            'farmer': instance.farmer.pin_inn,
        }

        # Check if the contour has associated crop yields
        if instance.crop_yields.exists():
            # Get the latest culture associated with this contour
            culture = instance.crop_yields.order_by("-year").first().culture

            # Add culture-related properties to the representation
            representation['properties']["culture"] = culture.name
            representation['properties']['crop_yield'] = round(culture.coefficient_crop * instance.area_ha, 2)
            representation['properties']['group'] = culture.name
            representation['properties']['fill_color'] = culture.fill_color
            representation['properties']['stroke_color'] = culture.stroke_color
        else:
            # If there are no associated crop yields, indicate it as "Unused land"
            representation['properties']['group'] = "Unused land"
            representation['properties']['fill_color'] = "#3388FF"
            representation['properties']['stroke_color'] = "#3388FF"

        return representation
