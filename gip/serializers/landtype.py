# Import the necessary serializers from the Django REST framework
from rest_framework import serializers

# Import the LandType model from the 'gip' application
from gip.models.contour import LandType

# Define a serializer for the LandType model
class LandTypeSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model that this serializer is associated with
        model = LandType

        # Exclude the 'name' field from the serialized representation
        exclude = ('name',)
