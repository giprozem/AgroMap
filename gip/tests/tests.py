import json
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase
from account.tests.factories import TokenFactory, AdminTokenFactory
from gip.tests.factories import (
    RegionFactory,
    DistrictFactory,
    ContonFactory,
    LandTypeFactory,
    SoilFactory,
    CultureFactory,
    ContourFactory,
    ContactInformationFactory,
    DepartmentFactory,
)
from rest_framework_gis.fields import GeoJsonDict
from django.contrib.gis.geos import GEOSGeometry


class TestGip(APITestCase):
    # This test case is used to test various endpoints related to geographic information.

    def test_region(self):
        # Test the '/gip/region/' endpoint to retrieve region data.
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
                "density": region.density,
            }
        ]
        response = self.client.get("/gip/region/")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_district(self):
        # Test the '/gip/district/' endpoint to retrieve district data.
        district = DistrictFactory()
        hour = int(district.created_at.strftime("%H"))
        hour += 6
        expected_data = [
            {
                "id": district.id,
                "created_at": district.created_at.strftime(
                    f"%Y-%m-%dT{hour}:%M:%S.%f+06:00"
                ),
                "updated_at": district.updated_at.strftime(
                    f"%Y-%m-%dT{hour}:%M:%S.%f+06:00"
                ),
                "code_soato_vet": district.code_soato_vet,
                "code_soato": district.code_soato,
                "name_ru": district.name,
                "name_ky": None,
                "name_en": None,
                "polygon": None,
                "region": district.region.id,
            }
        ]
        response = self.client.get("/gip/district/?polygon=true")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_conton(self):
        # Test the '/gip/conton/' endpoint to retrieve conton data.
        conton = ContonFactory()
        expected_data = [
            {
                "id": conton.id,
                "region": conton.district.region.id,
                "code_soato_vet": conton.code_soato_vet,
                "code_soato": conton.code_soato,
                "district": conton.district.id,
                "name_ru": conton.name,
                "name_ky": None,
                "name_en": None,
            }
        ]
        response = self.client.get("/gip/conton/")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_land_type(self):
        # Test the '/gip/land-type/' endpoint to retrieve land type data.
        land = LandTypeFactory()
        expected_data = [
            {"id": land.id, "name_ru": land.name, "name_ky": None, "name_en": None}
        ]
        response = self.client.get("/gip/land-type/")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_soil(self):
        # Test the '/gip/soil-class/' endpoint to retrieve soil data.
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
                "color": soil.color,
            }
        ]
        response = self.client.get("/gip/soil-class/")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_culture_get(self):
        # Test the '/gip/culture/' endpoint to retrieve culture data.
        culture = CultureFactory()
        expected_data = [
            {
                "id": culture.id,
                "name_ru": culture.name,
                "name_ky": None,
                "name_en": None,
                "coefficient_crop": culture.coefficient_crop,
            }
        ]
        response = self.client.get("/gip/culture/")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_culture_post(self):
        # Test the ability to create culture data using POST.
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        culture = CultureFactory()
        data = {"name": culture.name, "coefficient_crop": culture.coefficient_crop}
        response = self.client.post("/gip/culture/", data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_culture_put(self):
        # Test the ability to update culture data using PUT.
        self.token = AdminTokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        culture = CultureFactory()
        data = {"name": culture.name, "coefficient_crop": culture.coefficient_crop}
        response = self.client.put(f"/gip/culture/{culture.id}/", data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_culture_patch(self):
        # Test the ability to partially update culture data using PATCH.
        self.token = AdminTokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        culture = CultureFactory()
        data = {"coefficient_crop": culture.coefficient_crop}
        response = self.client.patch(f"/gip/culture/{culture.id}/", data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_culture_delete(self):
        # Test the ability to delete culture data.
        self.token = AdminTokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        culture = CultureFactory()
        response = self.client.delete(f"/gip/culture/{culture.id}/")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)


class TestGis(APITestCase):
    # This test case is used to test GIS-related endpoints.

    def _set_polygon(self):
        # Helper function to create a GeoJSON polygon for testing.
        polygon_data = {
            "type": "Polygon",
            "geometry": {
                "coordinates": [
                    [
                        [74.45802637350977, 42.960909912996755],
                        [74.45802637350977, 42.77960289493697],
                        [74.74107000893628, 42.77960289493697],
                        [74.74107000893628, 42.960909912996755],
                        [74.45802637350977, 42.960909912996755],
                    ]
                ],
            },
        }
        polygon = json.dumps(polygon_data)
        polygon_wkt = GEOSGeometry(polygon, srid=4326)
        return polygon_wkt

    def setUp(self) -> None:
        # Set up initial data, including a contour for testing.
        contour = ContourFactory()
        self.contour = contour

    def test_contour_get(self):
        # Test the ability to retrieve contour data.
        response = self.client.get(f"/gip/contour/{self.contour.id}/")
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_contour_destroy(self):
        # Test the ability to delete a contour.
        self.token = AdminTokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(f"/gip/contour/{self.contour.id}/")
        self.assertEqual(response.status_code, 200)


class DepartmentTestCase(APITestCase):
    # This test case is used to test endpoints related to departments.

    def setUp(self) -> None:
        # Set up initial department data for testing.
        department = DepartmentFactory()
        self.department = department

    def test_department_get(self):
        # Test the ability to retrieve department data.
        response = self.client.get("/gip/department/")
        self.assertEqual(response.status_code, 200)

    def test_department_post(self):
        # Test that POST requests to create departments are not allowed.
        query_data = {
            "unique_code": 123,
            "name": "test_department",
        }
        response = self.client.post("/gip/department/", query_data)
        self.assertEqual(response.data.get("detail"), 'Метод "POST" не разрешен.')

    def test_department_retrieve(self):
        # Test the ability to retrieve a specific department.
        response = self.client.get(f"/gip/department/{self.department.id}/")
        self.assertEqual(response.status_code, 200)


class ContactInformationTestCase(APITestCase):
    # This test case is used to test endpoints related to contact information.

    def setUp(self) -> None:
        # Set up initial contact information data for testing.
        contact = ContactInformationFactory()
        self.contact = contact

    def test_contact_info_get_ifquery(self):
        # Test the ability to retrieve contact information with query parameters.
        region_id = self.contact.district.region_id
        district_id = self.contact.district_id
        department_id = self.contact.department_id
        response = self.client.get(
            f"/gip/department/",
            {"region": region_id, "district": district_id, "department": department_id},
        )
        self.assertEqual(response.status_code, 200)

    def test_contact_info_ifqueryisnone(self):
        # Test the ability to retrieve contact information without query parameters.
        response = self.client.get("/gip/department/")
        self.assertEqual(response.status_code, 200)

    def test_contact_info_retrieve(self):
        # Test the ability to retrieve a specific contact information entry.
        response = self.client.get(f"/gip/department/{self.contact.id}/")
        self.assertEqual(response.status_code, 200)
