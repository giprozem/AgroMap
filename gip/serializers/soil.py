# Import serializers from the rest_framework_gis library
from rest_framework_gis import serializers

# Import the SoilClass model from the 'gip' application
from gip.models.soil import SoilClass

# Define a serializer for the SoilClass model
class SoilClassSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model that this serializer is associated with
        model = SoilClass

        # Exclude specific fields from the serialized representation
        exclude = ('created_at', 'updated_at', 'name', 'description')
