from rest_framework import serializers

from gip.models.contour import LandType


class LandTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandType
        exclude = ('name',)
