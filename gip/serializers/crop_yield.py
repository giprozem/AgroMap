from rest_framework import serializers

from gip.models import CropYield


class CropYieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropYield
        fields = '__all__'
