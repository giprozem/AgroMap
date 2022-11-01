from rest_framework import serializers

from plot.models import Plot, CultureField, Crop, SoilAnalysis


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
        exclude = ('culture_field', )


class CultureFieldSerializerInline(serializers.ModelSerializer):
    class Meta:
        model = CultureField
        # exclude = ('plot', )
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['crops'] = CropSerializer(instance.crops.all(), many=True).data
        representation['soil-analysis'] = SoilAnalysisInlineSerializer(instance.soil_analysis.all(), many=True).data
        return representation


class CultureFieldSerializerInlinePost(serializers.ModelSerializer):
    class Meta:
        model = CultureField
        exclude = ('id', )


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'


class SoilAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilAnalysis
        fields = '__all__'
