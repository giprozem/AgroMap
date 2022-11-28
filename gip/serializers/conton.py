from rest_framework import serializers

from gip.models import Conton


class ContonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conton
        fields = '__all__'
