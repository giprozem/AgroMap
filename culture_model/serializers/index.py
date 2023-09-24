# Import necessary modules and classes
from rest_framework.serializers import ModelSerializer
from culture_model.models.vegetation_index import VegetationIndex

# Create a serializer class named IndexSerializer
class IndexSerializer(ModelSerializer):
    class Meta:
        # Specify the model associated with the serializer
        model = VegetationIndex
        
        # Exclude specific fields ('name' and 'description') from serialization
        exclude = ('name', 'description')
