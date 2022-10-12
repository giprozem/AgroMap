from rest_framework import serializers

from plot.models import Plot, Culture


class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        fields = '__all__'


class CultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culture
        fields = '__all__'