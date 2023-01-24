from rest_framework.serializers import ModelSerializer

from culture_model.models.vegetation_index import VegetationIndex


class IndexSerializer(ModelSerializer):
    class Meta:
        model = VegetationIndex
        fields = '__all__'
