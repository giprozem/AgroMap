from rest_framework import serializers

from plot.models import Plot, Field, Crop, SoilAnalysis, Fertilizer


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


class SoilAnalysisInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilAnalysis
        # fields = '__all__'
        exclude = ('field', )


class FieldSerializerInline(serializers.ModelSerializer):
    class Meta:
        model = Field
        # exclude = ('plot', )
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['crops'] = CropSerializer(instance.crops.all(), many=True).data
        representation['soil-analysis'] = SoilAnalysisInlineSerializer(instance.soil_analysis.all(), many=True).data
        return representation


class FieldSerializerInlinePost(serializers.ModelSerializer):
    class Meta:
        model = Field
        exclude = ('id', )


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'


class SoilAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilAnalysis
        fields = '__all__'


class FertilizerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fertilizer
        fields = '__all__'
