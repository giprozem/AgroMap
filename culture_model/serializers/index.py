from rest_framework.serializers import ModelSerializer

from culture_model.models.index import Index


class IndexSerializer(ModelSerializer):
    class Meta:
        model = Index
        fields = '__all__'
