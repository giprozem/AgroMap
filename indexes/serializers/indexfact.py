from rest_framework import serializers

from culture_model.serializers.index import IndexSerializer
from indexes.models.indexfact import IndexFact, IndexMeaning


class IndexMeaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexMeaning
        fields = '__all__'


class IndexFactSerializer(serializers.ModelSerializer):
    meaning_of_average_value = IndexMeaningSerializer()
    index = IndexSerializer()

    class Meta:
        model = IndexFact
        fields = '__all__'
