import factory
from faker import Faker
from django.contrib.auth import get_user_model
from .models import CultureField, Plot, Crop, SoilAnalysis

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "test_1_user"


class PlotFactory(factory.django.DjangoModelFactory):
    class Meta:
         model = Plot
    user = factory.SubFactory(UserFactory)


class CultureFieldFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CultureField

    plot = factory.SubFactory(PlotFactory)
    what = 'test culture'
    start = Faker().date()


class CropFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Crop

    what = Faker().name()
    quantity = 1234
    unit = 'kg'
    start = Faker().date()
    culture = factory.SubFactory(CultureFieldFactory)


class SoilAnalysisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SoilAnalysis

    photo = factory.django.ImageField()
    date = Faker().date()
    description = Faker().name()
    culture_field = factory.SubFactory(CultureFieldFactory)
