from rest_framework import serializers

from indexes.models.actual_veg_index import ActualVegIndex


class VegIndexSerializer(serializers.ModelSerializer):
    index = serializers.CharField(source='index.name')

    class Meta:
        model = ActualVegIndex
        fields = ('index', 'average_value', )


# class ContourYearStatisticsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ContourYear
#         exclude = ('polygon', 'created_at', 'updated_at', )
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         result = VegIndexSerializer(instance.actual_veg_index.all(), many=True).data
#         for i in result:
#             representation[f'{i["index"]}'] = i['average_value']
#
#         return representation
