from rest_framework import serializers

from gip.models import Conton


class ContonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conton
        exclude = ('name', )


class ContonWithoutPolygonSerializer(serializers.ModelSerializer):
    polygon = serializers.NullBooleanField(default=False)

    class Meta:
        model = Conton
        exclude = ('name', 'created_at', 'updated_at',)
