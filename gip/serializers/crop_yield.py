# Import the necessary serializers from the Django REST framework
from rest_framework import serializers

# Import the CropYield model from the 'gip' application
from gip.models import CropYield

# Define a serializer for the CropYield model
class CropYieldSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model that this serializer is associated with
        model = CropYield

        # Include all fields from the model in the serialized representation
        fields = '__all__'
