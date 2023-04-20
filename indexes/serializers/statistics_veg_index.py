from rest_framework import serializers

from gip.models import Contour
from indexes.models.actual_veg_index import ActualVegIndex


class VegIndexSerializer(serializers.ModelSerializer):
    index = serializers.CharField(source='index.name')

    class Meta:
        model = ActualVegIndex
        fields = ('index', 'average_value', 'date',)


class ContourStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        exclude = (
            'polygon',
            'created_at',
            'updated_at',
            'code_soato',
            'area_ha',
            'is_deleted',
            'ink',
            'is_rounded',
            'farmer',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        result = VegIndexSerializer(instance.actual_veg_index.all(), many=True).data
        for i in result:
            representation[f'{i["index"]}'] = i['average_value']
            representation[f'{i["index"]}_date'] = i['date']

        return representation
