from rest_framework import serializers

from gip.models import Contour
from indexes.models.actual_veg_index import ActualVegIndex


class VegIndexSerializer(serializers.ModelSerializer):
    """
    A compact serializer for the ActualVegIndex model, specifically extracting the name of the index, its average value, and date.
    """
    index = serializers.CharField(source='index.name')

    class Meta:
        model = ActualVegIndex
        fields = ('index', 'average_value', 'date',)


"""
A serializer for the Contour model that excludes various fields. Additionally, it provides a custom representation which
incorporates data from associated VegIndex models.
"""


class ContourStatisticsSerializer(serializers.ModelSerializer):
    """
    A custom representation of the Contour instance which enhances the basic serialized data with additional vegetation index
    information.
    """

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
