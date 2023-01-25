from rest_framework import serializers

from culture_model.serializers.index import IndexSerializer
from indexes.models.actual_veg_index import ActuaVegIndex, IndexMeaning


class IndexMeaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexMeaning
        fields = '__all__'


class ActuaVegIndexSerializer(serializers.ModelSerializer):
    meaning_of_average_value = IndexMeaningSerializer()
    index = IndexSerializer()

    class Meta:
        model = ActuaVegIndex
        fields = '__all__'


class SatelliteImageSerializer(serializers.ModelSerializer):
    index = IndexSerializer()

    class Meta:
        model = ActuaVegIndex
        fields = '__all__'
