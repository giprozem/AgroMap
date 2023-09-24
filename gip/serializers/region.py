# Import serializers from the rest_framework_gis library
from rest_framework_gis import serializers

# Import the Region model from the 'gip' application
from gip.models import Region

# Define a serializer for the Region model
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model that this serializer is associated with
        model = Region

        # Exclude the 'name' field from the serialized representation
        exclude = ('name',)

# Define another serializer for the Region model without the 'polygon' and other specified fields
class RegionWithoutPolygonSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model that this serializer is associated with
        model = Region

        # Exclude the 'polygon', 'name', 'created_at', and 'updated_at' fields from the serialized representation
        exclude = ('polygon', 'name', 'created_at', 'updated_at',)
