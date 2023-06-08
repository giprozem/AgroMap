from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase
from gip.tests.factories import RegionFactory, DistrictFactory, ContonFactory, LandTypeFactory
from django.test import Client


class TestGip(APITestCase):

    def test_region(self):
        region = RegionFactory()
        expected_data = [
            {
                "id": region.id,
                "code_soato": region.code_soato,
                "name_ru": region.name,
                "name_ky": None,
                "name_en": None,
                "population": region.population,
                "area": region.area,
                "density": region.density
            }
        ]
        response = self.client.get('/gip/region/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_district(self):
        district = DistrictFactory()
        hour = int(district.created_at.strftime('%H'))
        hour += 6
        expected_data = [
            {
                "id": district.id,
                "created_at": district.created_at.strftime(f'%Y-%m-%dT{hour}:%M:%S.%f+06:00'),
                "updated_at": district.updated_at.strftime(f'%Y-%m-%dT{hour}:%M:%S.%f+06:00'),
                "code_soato": district.code_soato,
                "name_ru": district.name,
                "name_ky": None,
                "name_en": None,
                "polygon": None,
                "region": district.region.id
            }
        ]
        response = self.client.get('/gip/district/?polygon=true')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_conton(self):
        conton = ContonFactory()
        expected_data = [
            {
                "id": conton.id,
                "region": conton.district.region.id,
                "code_soato": conton.code_soato,
                "district": conton.district.id,
                "name_ru": conton.name,
                "name_ky": None,
                "name_en": None
            }
        ]
        response = self.client.get('/gip/conton/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_land_type(self):
        land = LandTypeFactory()
        expected_data = [
            {
                "id": land.id,
                "name_ru": land.name,
                "name_ky": None,
                "name_en": None
            }
        ]
        response = self.client.get('/gip/land-type/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
