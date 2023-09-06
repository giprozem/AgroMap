import json

from rest_framework.test import APITestCase, APIClient
from gip.tests.factories import ContourFactory
from indexes.models import ProductivityClass
from django.contrib.gis.geos import GEOSGeometry


class CreatingAverageApiTestCase(APIClient):
    _URL_ = "/veg/average/"

    def setUp(self) -> None:
        contour = ContourFactory()
        productivity = ProductivityClass(
            name="test_productivity",
            description="test_prod_desc"
        )
        productivity.save()
        self.contour = contour

    def test_pasture_status_code_ifquerynone(self):
        self.client = APIClient(raise_request_exception=False)
        response = self.client.get(self._URL_)
        self.assertEqual(response.status_code, 500)

    def test_pasture_ifquery(self):
        response = self.client.get(self._URL_, {"start": "2023-07-30", "end": "2023-08-30"})
        self.assertEqual(response.status_code, 200)