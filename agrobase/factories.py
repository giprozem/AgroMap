import factory
from faker import Faker
from factory import fuzzy

from agrobase.models import Material, MaterialBlock, MaterialImage


class MaterialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Material

    category = 2


class MaterialBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MaterialBlock

    material = factory.SubFactory(MaterialFactory)
    title = Faker().name()
    text = Faker().text()
    image = factory.django.ImageField(color='blue')


class MaterialImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MaterialImage

    material = factory.SubFactory(MaterialFactory)
    image = factory.django.ImageField(color='blue')
