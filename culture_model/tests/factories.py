# Import necessary modules and classes
from factory.django import DjangoModelFactory
from factory import SubFactory
from faker import Faker
from culture_model.models.vegetation_index import VegetationIndex

# Create a factory class named VegetationIndexFactory
class VegetationIndexFactory(DjangoModelFactory):
    class Meta:
        # Specify the model associated with the factory
        model = VegetationIndex

    # Define factory attributes
    name = Faker().name()          # Generate a fake name
    description = Faker().text()   # Generate fake text for description
