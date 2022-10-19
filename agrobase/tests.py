import os
import shutil
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from agrobase.factories import MaterialFactory, MaterialBlockFactory, MaterialImageFactory
from config.settings import BASE_DIR


TEST_DIR = 'test_data'


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


class MaterialBlockTest(APITestCase):

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_get_block_success_200(self):
        b1 = MaterialBlockFactory()

        response = self.client.get(f'/agro_base/block/{b1.id}/')
        self.assertEqual(response.status_code, HTTP_200_OK)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_create_block_success_201(self):
        b1 = MaterialBlockFactory()
        expected_data = {
            "id": b1.id,
            "material": b1.material.id,
            "title": b1.title,
            "text": b1.text,
            "image": b1.image
        }

        response = self.client.post('/agro_base/block/', expected_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_update_block_success_200(self):
        b1 = MaterialBlockFactory()
        expected_data = {
            'material': b1.material.id,
            "title": 'b1.title',
            "text": 'b1.text',
            "image": b1.image
        }

        response = self.client.put(f'/agro_base/block/{b1.id}/', expected_data)
        print(response.data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_delete_block_success_204(self):
        b1 = MaterialBlockFactory()
        response = self.client.delete(f"/agro_base/block/{b1.id}/")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_delete_image(self):
        images_path = os.path.join(BASE_DIR, 'media/material_block_images')
        files = [i for i in os.listdir(images_path)
                 if os.path.isfile(os.path.join(images_path, i))
                 and i.startswith('example')]
        for file in files:
            os.remove(os.path.join(images_path, file))

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass


class MaterialImageTest(APITestCase):

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_get_image_success_200(self):
        i1 = MaterialImageFactory()
        expected_data = {
            "id": i1.id,
            "material": i1.material.id,
            'image': i1.image
        }

        response = self.client.get(f'/agro_base/image/{i1.id}/')
        self.assertEqual(response.status_code, HTTP_200_OK)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_create_image_success_201(self):
        i1 = MaterialImageFactory()
        expected_data = {
            "material": i1.material.id,
            'image': i1.image
        }

        response = self.client.post(f'/agro_base/image/', expected_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_update_image_success_200(self):
        i1 = MaterialImageFactory()
        expected_data = {
            "material": i1.material.id,
            'image': i1.image
        }

        response = self.client.put(f'/agro_base/image/{i1.id}/', expected_data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_delete_image_success_204(self):
        i1 = MaterialImageFactory()
        response = self.client.delete(f'/agro_base/image/{i1.id}/')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
