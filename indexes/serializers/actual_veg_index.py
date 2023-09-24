from rest_framework import serializers

from culture_model.serializers.index import IndexSerializer
from indexes.models.actual_veg_index import ActualVegIndex, IndexMeaning, PredictedContourVegIndex


class IndexMeaningSerializer(serializers.ModelSerializer):
    """
    A serializer for the IndexMeaning model. Excludes certain fields.
    """

    class Meta:
        model = IndexMeaning
        exclude = ('min_index_value', 'max_index_value', 'description')


class ActuaVegIndexSerializer(serializers.ModelSerializer):
    """
    A serializer for the ActualVegIndex model, encompassing all of its fields and nested fields for associated models.
    """
    meaning_of_average_value = IndexMeaningSerializer()
    index = IndexSerializer()

    class Meta:
        model = ActualVegIndex
        fields = '__all__'


class SatelliteImageSerializer(serializers.ModelSerializer):
    """
    A serializer for the SatelliteImage, which is essentially the same as ActualVegIndex serializer. Encompasses all fields.
    """
    index = IndexSerializer()

    class Meta:
        model = ActualVegIndex
        fields = '__all__'


class PredictedContourActuaVegIndexSerializer(serializers.ModelSerializer):
    """
    A serializer for the PredictedContourVegIndex model. Again, includes all fields and nested fields for associated models.
    """
    meaning_of_average_value = IndexMeaningSerializer()
    index = IndexSerializer()

    class Meta:
        model = PredictedContourVegIndex
        fields = '__all__'
