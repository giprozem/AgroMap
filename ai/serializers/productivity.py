from rest_framework import serializers

from ai.models.predicted_contour import Contour_AI
from indexes.serializers.statistics_veg_index import VegIndexSerializer


class ContourAISerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour_AI
        fields = '__all__'


class ContourAIStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour_AI
        exclude = ('polygon', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(instance)
        result = VegIndexSerializer(instance.contour_ai_veg_index.all(), many=True).data
        for i in result:
            representation[f'{i["index"]}'] = i['average_value']

        return representation
