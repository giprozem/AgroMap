from rest_framework import serializers

from plot.models import Plot, CultureField, Crop, Fertilizer


class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['cultures'] = CultureSerializerInline(instance.cultures.all(), many=True).data
    #     return representation


class PlotCultureFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['cultures'] = CultureSerializerInline(instance.cultures.all(), many=True).data
    #     return representation


class CultureFieldSerializerInline(serializers.ModelSerializer):
    class Meta:
        model = CultureField
        # exclude = ('plot', )
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['crops'] = CropSerializer(instance.crops.all(), many=True).data
        return representation


class CultureFieldSerializerInlinePost(serializers.ModelSerializer):
    class Meta:
        model = CultureField
        exclude = ('id', )


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'


class FertilizerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fertilizer
        fields = '__all__'
