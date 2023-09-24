# Import serializers from the rest_framework_gis library
from rest_framework_gis import serializers

# Import the District model from the 'gip' application
from gip.models import District

# Define a serializer for the District model
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model that this serializer is associated with
        model = District

        # Exclude the 'name' field from the serialized representation
        exclude = ('name',)

# Define another serializer for the District model without the 'polygon' and other specified fields
class DistrictWithoutPolygonSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model that this serializer is associated with
        model = District

        # Exclude the 'polygon', 'created_at', 'updated_at', and 'name' fields from the serialized representation
        exclude = ('polygon', 'created_at', 'updated_at', 'name',)
