import random

from django.contrib.gis.geos import GEOSGeometry
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from django.contrib.auth import get_user_model
from django.test import override_settings

from hub.models import LandInfo, PropertyTypeList, DocumentTypeList, CategoryTypeList, LandTypeList

User = get_user_model()

TEST_DIR = 'test_data'


class CultureTests(APITestCase):
    def setUp(self):
        contour = {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        74.398127,
                        42.855267
                    ],
                    [
                        74.398127,
                        42.864264
                    ],
                    [
                        74.414692,
                        42.864264
                    ],
                    [
                        74.414692,
                        42.855267
                    ],
                    [
                        74.398127,
                        42.855267
                    ]
                ]
            ]
        }
        property_type = PropertyTypeList.objects.create(type_name='Частный')
        document_type = DocumentTypeList.objects.create(type_name='Правоустанавливающие документы')
        category_type = CategoryTypeList.objects.create(type_name='С/х земля')
        land_type = LandTypeList.objects.create(type_name='Пастбища')
        land_info = LandInfo.objects.create(ink=f"417-02-123-456-78-{random.randint(1200,9999)}", eni=f"417-02-123-456-78-{random.randint(1, 100)}",
                     inn_pin=f"20220515{random.randint(1, 100)}", bonitet=random.randint(1, 100), culture='Картофель', crop_yield=10.2,
                     property_type=property_type, document_type=document_type, document_link='', category_type=category_type, land_type=land_type, square=200,
                     contour=GEOSGeometry(contour))
        print(land_info)

        self.land_info = land_info

    def test_get_land_info_success_200(self):
        li = self.land_info
        expected_data = [
            {
                "id": li.id,
                "ink": li.ink,
                "eni": li.eni,
                "inn_pin": li.inn_pin,
                "bonitet": li.bonitet,
                "crop_yield": li.crop_yield,
                "property_type": li.property_type,
                "document_type": li.document_type,
                "document_link": li.document_link,
                "category_type": li.category_type,
                "square": li.square
            },
        ]
        response = self.client.get(f"/zem_balance/{self.id}/")
        print(response)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data, 'Dannye ne sovpadaut')

