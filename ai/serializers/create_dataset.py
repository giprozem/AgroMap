from rest_framework import serializers
from ai.models.create_dataset import CreateDescription


class CreateDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateDescription
        exclude = ('description',)
