from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase
from culture_model.tests.factories import VegetationIndexFactory
from django.test import Client


class TestCulture(APITestCase):

    def test_index(self):
        response = self.client.get('/info/index-list/')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        veg = VegetationIndexFactory()
        response = self.client.get('/info/index-list/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        expected_data = [
            {
                "id": veg.id,
                "name_ru": veg.name,
                "name_ky": None,
                "name_en": None,
                "description_ru": veg.description,
                "description_ky": None,
                "description_en": None
            }
        ]
        self.assertEqual(response.data, expected_data)
