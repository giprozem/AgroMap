from rest_framework_gis import serializers
from gip.models.soil import SoilClass


class SoilClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilClass
        exclude = ('created_at', 'updated_at', 'name', 'description')
