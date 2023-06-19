from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase
from account.tests.factories import TokenFactory, AdminTokenFactory
from gip.tests.factories import RegionFactory, DistrictFactory, ContonFactory, LandTypeFactory, \
    SoilFactory, CultureFactory, ContourFactory
from rest_framework_gis.fields import GeoJsonDict


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

    def test_soil(self):
        soil = SoilFactory()
        expected_data = [
            {
                "id": soil.id,
                "id_soil": soil.id_soil,
                "name_ru": soil.name,
                "name_ky": None,
                "name_en": None,
                "description_ru": soil.description,
                "description_ky": None,
                "description_en": None,
                "color": soil.color
            }
        ]
        response = self.client.get('/gip/soil-class/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_culture_get(self):
        culture = CultureFactory()
        expected_data = [
            {
                "id": culture.id,
                "name_ru": culture.name,
                "name_ky": None,
                "name_en": None,
                "coefficient_crop": culture.coefficient_crop
            }
        ]
        response = self.client.get('/gip/culture/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_culture_post(self):
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        culture = CultureFactory()
        data = {
            "name": culture.name,
            "coefficient_crop": culture.coefficient_crop
        }
        response = self.client.post('/gip/culture/', data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_culture_put(self):
        self.token = AdminTokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        culture = CultureFactory()
        data = {
            "name": culture.name,
            "coefficient_crop": culture.coefficient_crop
        }
        response = self.client.put(f'/gip/culture/{culture.id}/', data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_culture_patch(self):
        self.token = AdminTokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        culture = CultureFactory()
        data = {
            "coefficient_crop": culture.coefficient_crop
        }
        response = self.client.patch(f'/gip/culture/{culture.id}/', data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_culture_delete(self):
        self.token = AdminTokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        culture = CultureFactory()
        response = self.client.delete(f'/gip/culture/{culture.id}/')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)


class TestGis(APITestCase):

    def test_contour_get(self):
        contour = ContourFactory()
        hour = int(contour.created_at.strftime('%H'))
        hour += 6
        expected_data = {
            "id": contour.id,
            "year": None,
            "code_soato": contour.code_soato,
            "ink": None,
            "created_at": contour.created_at.strftime(f'%Y-%m-%dT{hour}:%M:%S.%f+06:00'),
            "updated_at": contour.updated_at.strftime(f'%Y-%m-%dT{hour}:%M:%S.%f+06:00'),
            "polygon": GeoJsonDict((
                ('type', contour.polygon.geom_type),
                ('coordinates', [[list(i) for i in contour.polygon.coords[0]]]),
            )),
            "productivity": None,
            "predicted_productivity": None,
            "area_ha": contour.area_ha,
            "is_deleted": False,
            "elevation": str(contour.elevation),
            "is_rounded": False,
            "conton": {
                "id": contour.conton.id,
                "name_ru": contour.conton.name,
                "name_ky": None,
                "name_en": None,
                "code_soato": contour.conton.code_soato
            },
            "type": {
                "id": contour.type.id,
                "name_ru": contour.type.name,
                "name_ky": None,
                "name_en": None
            },
            "culture": {
                "id": None,
                "name_ru": None,
                "name_ky": None,
                "name_en": None,
                "coefficient_crop": None
            },
            "farmer": None,
            "soil_class": {
                "id": None,
                "id_soil": None,
                "name_ru": None,
                "name_ky": None,
                "name_en": None,
                "description_ru": None,
                "description_ky": None,
                "description_en": None,
                "color": None
            },
            "pasture_culture": [],
            "region": {
                "id": contour.conton.district.region.id,
                "name_ru": contour.conton.district.region.name,
                "name_ky": None,
                "name_en": None,
                "code_soato": contour.conton.district.region.code_soato
            },
            "district": {
                "id": contour.conton.district.id,
                "name_ru": contour.conton.district.name,
                "name_ky": None,
                "name_en": None,
                "code_soato": contour.conton.district.code_soato
            }
        }
        response = self.client.get(f'/gip/contour/{contour.id}/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
