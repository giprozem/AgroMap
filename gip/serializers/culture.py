# Import the necessary serializers from the Django REST framework
from rest_framework import serializers

# Import the Culture model from the 'gip' application
from gip.models import Culture

# Define a serializer for the Culture model
class CultureSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model that this serializer is associated with
        model = Culture

        # Exclude specific fields from the serialized representation
        exclude = ('name', 'created_at', 'updated_at',)
