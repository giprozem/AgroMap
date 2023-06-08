from factory.django import DjangoModelFactory
from factory import SubFactory
from faker import Faker
from gip.models.region import Region
from gip.models.district import District
from gip.models.conton import Conton
from gip.models.contour import LandType


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = Region

    code_soato = Faker().pystr(max_chars=30)
    name = Faker().name()
    population = Faker().pyint()
    area = Faker().pyint()
    density = Faker().pyfloat()


class DistrictFactory(DjangoModelFactory):
    class Meta:
        model = District

    code_soato = Faker().pystr(max_chars=30)
    region = SubFactory(RegionFactory)
    name = Faker().name()


class ContonFactory(DjangoModelFactory):
    class Meta:
        model = Conton

    code_soato = Faker().pystr(max_chars=30)
    district = SubFactory(DistrictFactory)
    name = Faker().name()


class LandTypeFactory(DjangoModelFactory):
    class Meta:
        model = LandType

    name = Faker().name()
