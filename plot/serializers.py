from rest_framework import serializers

from plot.models import Plot, Culture


class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['cultures'] = CultureSerializerInline(instance.cultures.all(), many=True).data
    #     return representation


class PlotCultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['cultures'] = CultureSerializerInline(instance.cultures.all(), many=True).data
    #     return representation


class CultureSerializerInline(serializers.ModelSerializer):
    class Meta:
        model = Culture
        # exclude = ('plot', )
        fields = '__all__'


class CultureSerializerInlinePost(serializers.ModelSerializer):
    class Meta:
        model = Culture
        exclude = ('id', )
