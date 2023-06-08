from factory.django import DjangoModelFactory
from factory import SubFactory
from faker import Faker
from culture_model.models.vegetation_index import VegetationIndex


class VegetationIndexFactory(DjangoModelFactory):
    class Meta:
        model = VegetationIndex

    name = Faker().name()
    description = Faker().text()
