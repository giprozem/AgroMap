import json

from faker import Faker
from rest_framework.test import APITestCase, APIClient
from django.contrib.gis.geos import GEOSGeometry

from indexes.models.actual_veg_index import ActualVegIndex, PredictedContourVegIndex
from culture_model.models.vegetation_index import VegetationIndex


from gip.tests.factories import ContourFactory


class ContourStatisticTestCase(APITestCase):
    _URL_ = "/veg/contour-veg-index-statistics/"

    def setUp(self) -> None:
        contour = ContourFactory()
        self.contour = contour
    
    def test_if_dataisnone(self):
        self.client = APIClient(raise_request_exception=False)
        response = self.client.get(self._URL_)
        self.assertEqual(response.status_code, 500)

    def test_ifData(self):
        response = self.client.get(self._URL_, {"start": "2023-08-15", "end":"2023-08-16"})
        self.assertEqual(response.status_code, 200)