from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from agrobase.factories import MaterialFactory


class MaterialTest(APITestCase):

    def test_get_material_success_200(self):
        m1 = MaterialFactory()
        expected_data = {
            "id": m1.id,
            "category": {'id': '2',
                         'title': 'Насекомые'},
            'images': [],
            'blocks': []
        }

        response = self.client.get(f'/agro_base/material/{m1.id}/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data, 'Данные не совпадают')

    def test_create_material_success_201(self):
        m1 = MaterialFactory()
        expected_data = {
            "id": m1.id,
            "category": 2,
        }

        response = self.client.post(f'/agro_base/material/', expected_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_update_material_success_200(self):
        m1 = MaterialFactory()
        expected_data = {
            "category": 1,
        }

        response = self.client.put(f"/agro_base/material/{m1.id}/", expected_data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_deleted_material_success_204(self):
        m1 = MaterialFactory()

        response = self.client.delete(f"/agro_base/material/{m1.id}/")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)