from factory.django import DjangoModelFactory
from factory import SubFactory
from faker import Faker

from gip.models.region import Region
from gip.models.district import District
from gip.models.conton import Conton
from gip.models.contour import LandType
from gip.models.soil import SoilClass
from gip.models.culture import Culture
from gip.models.contour import Contour
from gip.tests.polygon import get_polygon
from gip.models.contact_information import Department, ContactInformation


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
    code_soato_vet = Faker().pystr(max_chars=30)
    region = SubFactory(RegionFactory)
    name = Faker().name()


class ContonFactory(DjangoModelFactory):
    class Meta:
        model = Conton

    code_soato = Faker().pystr(max_chars=30)
    code_soato_vet = Faker().pystr(max_chars=30)
    district = SubFactory(DistrictFactory)
    name = Faker().name()


class LandTypeFactory(DjangoModelFactory):
    class Meta:
        model = LandType

    name = Faker().name()


class SoilFactory(DjangoModelFactory):
    class Meta:
        model = SoilClass

    id_soil = Faker().pyint()
    name = Faker().name()
    description = Faker().text()
    color = Faker().hex_color()


class CultureFactory(DjangoModelFactory):
    class Meta:
        model = Culture

    name = Faker().name()
    coefficient_crop = Faker().pyfloat()


class ContourFactory(DjangoModelFactory):
    class Meta:
        model = Contour

    ink = Faker().pystr(max_chars=20)
    culture = SubFactory(CultureFactory)
    code_soato = Faker().pystr(max_chars=30)
    conton = SubFactory(ContonFactory)
    type = SubFactory(LandTypeFactory)
    polygon = get_polygon()
    year = 2022


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    unique_code = Faker().pyint()
    name = Faker().pystr(max_chars=30)


class ContactInformationFactory(DjangoModelFactory):
    class Meta:
        model = ContactInformation

    department = SubFactory(DepartmentFactory)
    title = Faker().pystr(max_chars=30)
    fullname = Faker().pystr(max_chars=30)
    district = SubFactory(DistrictFactory)
    address = Faker().pystr(max_chars=30)
    phone = Faker().pyint()
    mail = Faker().pystr(max_chars=30)
