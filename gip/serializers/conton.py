from rest_framework import serializers
from gip.models import Conton, Region

# Serializer for the Conton model with region information
class ContonSerializer(serializers.ModelSerializer):
    # Add a custom field 'region' using SerializerMethodField
    region = serializers.SerializerMethodField()

    # Define a method to get the region information for the Conton instance
    def get_region(self, obj):
        region = Region.objects.get(name=obj.district.region)
        return region.pk  # Return the primary key of the region

    class Meta:
        model = Conton  # Specify the model to serialize
        exclude = ('name',)  # Exclude the 'name' field from serialization

# Serializer for the Conton model without polygon information
class ContonWithoutPolygonSerializer(serializers.ModelSerializer):
    # Add a custom field 'region' using SerializerMethodField
    region = serializers.SerializerMethodField()

    # Define a method to get the region information for the Conton instance
    def get_region(self, obj):
        region = Region.objects.get(name=obj.district.region)
        return region.pk  # Return the primary key of the region

    class Meta:
        model = Conton  # Specify the model to serialize
        exclude = ('polygon', 'name', 'created_at', 'updated_at',)  # Exclude specific fields from serialization
