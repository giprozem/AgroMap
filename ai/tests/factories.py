from factory.django import DjangoModelFactory, FileField
from faker import Faker
from factory import SubFactory

from ai.models.create_dataset import Process, CreateDescription
from indexes.models.actual_veg_index import PredictedContourVegIndex
from culture_model.models import VegetationIndex
from gip.tests.test_additional_views import Contour_AIFactory
from ai.models import Yolo



class ProcessFactory(DjangoModelFactory):
    class Meta:
        model = Process

    is_running = True
    type_of_process = Faker().pyint()


class VegetationIndexFactory(DjangoModelFactory):
    class Meta:
        model = VegetationIndex

    name = Faker().pystr(max_chars=30)
    description = Faker().pystr(max_chars=30)


class PredictedContourVegIndexFactory(DjangoModelFactory):
    class Meta:
        model = PredictedContourVegIndex

    average_value = 10.00
    contour = SubFactory(Contour_AIFactory)
    date = "2023-05-05"
    index = SubFactory(VegetationIndexFactory)


class YoloFactory(DjangoModelFactory):
    class Meta:
        model = Yolo
    
    ai = FileField(filename='test_file.zip')


class CreateDescriptionFactory(DjangoModelFactory):
    
    class Meta:
        model = CreateDescription

    description = Faker().pystr(max_chars=30)