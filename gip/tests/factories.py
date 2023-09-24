# Import necessary modules from Factory Boy and Faker libraries
from factory.django import DjangoModelFactory
from factory import SubFactory
from faker import Faker

# Import Django models from the 'gip' application
from gip.models.region import Region
from gip.models.district import District
from gip.models.conton import Conton
from gip.models.contour import LandType
from gip.models.soil import SoilClass
from gip.models.culture import Culture
from gip.models.contour import Contour
from gip.tests.polygon import get_polygon
from gip.models.contact_information import Department, ContactInformation

# Define a factory for generating test data for the Region model
class RegionFactory(DjangoModelFactory):
    class Meta:
        model = Region

    # Generate random data for the Region model fields
    code_soato = Faker().pystr(max_chars=30)
    name = Faker().name()
    population = Faker().pyint()
    area = Faker().pyint()
    density = Faker().pyfloat()

# Define a factory for generating test data for the District model
class DistrictFactory(DjangoModelFactory):
    class Meta:
        model = District

    # Generate random data for the District model fields
    code_soato = Faker().pystr(max_chars=30)
    code_soato_vet = Faker().pystr(max_chars=30)
    region = SubFactory(RegionFactory)
    name = Faker().name()

# Define a factory for generating test data for the Conton model
class ContonFactory(DjangoModelFactory):
    class Meta:
        model = Conton

    # Generate random data for the Conton model fields
    code_soato = Faker().pystr(max_chars=30)
    code_soato_vet = Faker().pystr(max_chars=30)
    district = SubFactory(DistrictFactory)
    name = Faker().name()

# Define a factory for generating test data for the LandType model
class LandTypeFactory(DjangoModelFactory):
    class Meta:
        model = LandType

    # Generate random data for the LandType model fields
    name = Faker().name()

# Define a factory for generating test data for the SoilClass model
class SoilFactory(DjangoModelFactory):
    class Meta:
        model = SoilClass

    # Generate random data for the SoilClass model fields
    id_soil = Faker().pyint()
    name = Faker().name()
    description = Faker().text()
    color = Faker().hex_color()

# Define a factory for generating test data for the Culture model
class CultureFactory(DjangoModelFactory):
    class Meta:
        model = Culture

    # Generate random data for the Culture model fields
    name = Faker().name()
    coefficient_crop = Faker().pyfloat()

# Define a factory for generating test data for the Contour model
class ContourFactory(DjangoModelFactory):
    class Meta:
        model = Contour

    # Generate random data for the Contour model fields
    ink = Faker().pystr(max_chars=20)
    culture = SubFactory(CultureFactory)
    code_soato = Faker().pystr(max_chars=30)
    conton = SubFactory(ContonFactory)
    type = SubFactory(LandTypeFactory)
    polygon = get_polygon()
    year = 2022

# Define a factory for generating test data for the Department model
class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    # Generate random data for the Department model fields
    unique_code = Faker().pyint()
    name = Faker().pystr(max_chars=30)

# Define a factory for generating test data for the ContactInformation model
class ContactInformationFactory(DjangoModelFactory):
    class Meta:
        model = ContactInformation

    # Generate random data for the ContactInformation model fields
    department = SubFactory(DepartmentFactory)
    title = Faker().pystr(max_chars=30)
    fullname = Faker().pystr(max_chars=30)
    district = SubFactory(DistrictFactory)
    address = Faker().pystr(max_chars=30)
    phone = Faker().pyint()
    mail = Faker().pystr(max_chars=30)
