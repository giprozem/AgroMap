from rest_framework import serializers
from ai.models.create_dataset import CreateDescription

# Serializer for CreateDescription model
class CreateDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateDescription
        exclude = ('description',)  # Exclude the 'description' field from serialization

