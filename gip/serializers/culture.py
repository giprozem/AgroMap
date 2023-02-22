from rest_framework import serializers

from gip.models import Culture


class CultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culture
        exclude = ('name',)
