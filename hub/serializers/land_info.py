# Import necessary modules and classes from Django REST framework
from rest_framework import serializers

# Import GeoFeatureModelSerializer for geographic data serialization
from rest_framework_gis.serializers import GeoFeatureModelSerializer

# Import the "LandInfo" model from the "hub" app
from hub.models import LandInfo

# Serializer for "ZemBalance" with all fields
class ZemBalanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = LandInfo
        fields = '__all__'

# Serializer for "LandInfo" with geographic data support
class LandInfoSerializers(GeoFeatureModelSerializer):
    class Meta:
        model = LandInfo
        fields = '__all__'
        geo_field = 'main_map'  # Specify the geographic field for GeoJSON serialization

# Custom search serializer for "LandInfo" with only the 'ink_code' field
class LandInfoCustomSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandInfo
        fields = ('ink_code', )