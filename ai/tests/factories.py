from factory.django import DjangoModelFactory
from faker import Faker
from factory import SubFactory

from ai.models.create_dataset import Process, CreateDescription
from ai.models.predicted_contour import Contour_AI
from gip.tests.factories import ContonFactory, LandTypeFactory, CultureFactory, get_polygon
from indexes.models.actual_veg_index import PredictedContourVegIndex
from culture_model.models import VegetationIndex

# Factory for creating Contour_AI instances
class Contour_AIFactory(DjangoModelFactory):
    conton = SubFactory(ContonFactory)
    polygon = get_polygon()
    year = 2022
    productivity = 1
    type = SubFactory(LandTypeFactory)
    culture = SubFactory(CultureFactory)

    class Meta:
        model = Contour_AI

# Factory for creating Process instances
class ProcessFactory(DjangoModelFactory):
    class Meta:
        model = Process

    is_running = True
    type_of_process = Faker().pyint()

# Factory for creating VegetationIndex instances
class VegetationIndexFactory(DjangoModelFactory):
    class Meta:
        model = VegetationIndex

    name = Faker().pystr(max_chars=30)
    description = Faker().pystr(max_chars=30)

# Factory for creating PredictedContourVegIndex instances
class PredictedContourVegIndexFactory(DjangoModelFactory):
    class Meta:
        model = PredictedContourVegIndex

    average_value = 10.00
    contour = SubFactory(Contour_AIFactory)
    date = "2023-05-05"
    index = SubFactory(VegetationIndexFactory)

# Factory for creating CreateDescription instances
class CreateDescriptionFactory(DjangoModelFactory):
    
    class Meta:
        model = CreateDescription

    description = Faker().pystr(max_chars=30)
