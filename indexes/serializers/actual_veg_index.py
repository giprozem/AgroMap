from rest_framework import serializers

from culture_model.serializers.index import IndexSerializer
from indexes.models.actual_veg_index import ActualVegIndex, IndexMeaning


class IndexMeaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexMeaning
        exclude = ('min_index_value', 'max_index_value', )


class ActuaVegIndexSerializer(serializers.ModelSerializer):
    meaning_of_average_value = IndexMeaningSerializer()
    index = IndexSerializer()

    class Meta:
        model = ActualVegIndex
        fields = '__all__'


class SatelliteImageSerializer(serializers.ModelSerializer):
    index = IndexSerializer()

    class Meta:
        model = ActualVegIndex
        fields = '__all__'
