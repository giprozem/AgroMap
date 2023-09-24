from rest_framework import serializers

from ai.models.predicted_contour import Contour_AI
from indexes.serializers.statistics_veg_index import VegIndexSerializer


# Serializer for Contour_AI model
class ContourAISerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour_AI
        fields = '__all__'  # Serialize all fields from the Contour_AI model


# Serializer for Contour_AI model with statistics
class ContourAIStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour_AI
        exclude = ('polygon',)  # Exclude the 'polygon' field from serialization

    # Custom representation method to include additional statistics
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Calculate and add statistics for veg index data
        result = VegIndexSerializer(instance.contour_ai_veg_index.all(), many=True).data
        for i in result:
            representation[f'{i["index"]}'] = i['average_value']

        return representation
