import json

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from elevation.data import elevation
from hub.models.land_info import LandInfo

from gip.models.conton import Conton
from gip.models.district import District
from gip.models.region import Region


User = get_user_model()

TEST_DIR = "test_data"


class CultureTests(APITestCase):
    _URL_ = "/hub/elevation/"
    reponse_data = None
    geometry_map = {"latitude": [38, 44], "longitude": [69, 81]}
    latitude = geometry_map.get("latitude")[1]
    longitude = geometry_map.get("longitude")[1]

    def setUp(self) -> None:
        elevation_data = elevation(
            latitude=float(self.latitude), longitude=float(self.longitude)
        )
        self.reponse_data = {"elevation": elevation_data.tolist()}

    def test_status_code_elevation_soil_view(self):
        response = self.client.get(self._URL_, self.geometry_map)
        self.assertEqual(response.status_code, 200)

    def test_reponse_content_elevation_soil_view(self):
        response = self.client.get(self._URL_, self.geometry_map)
        response_data = json.loads(response.content)
        self.assertEqual(
            self.reponse_data.get("elevation"), response_data.get("elevation")
        )


class LandInfoSearchTestCase(APITestCase):
    _URL_ = "/hub/search_ink_hub/"

    def setUp(self) -> None:
        land_info = LandInfo(ink_code="test_inc_code")
        land_info.save()
        self.land_info = land_info

    def test_search_if_queryisnone(self):
        response = self.client.get(self._URL_)
        self.assertEqual(response.data, [])

    def test_search_if_query(self):
        response = self.client.get(self._URL_, {"search": "test"})
        self.assertEqual(len(response.data.get("list_ink_code")), 1)


class AmountCattleApiTestCase(APITestCase):
    _URL_ = "/hub/amount_cattle/"

    def setUp(self) -> None:
        region = Region(
            code_soato=11111,
            name="test_region_name",
            population="1",
            area="2",
            density="2",
        )
        region.save()
        district = District(
            code_soato_vet=41711,
            code_soato=11111,
            name="test_district_name",
            region=region,
        )
        district.save()
        self.canton = Conton(
            code_soato_vet=41711,
            code_soato=11111,
            district=district,
            name="test_conton_name",
        )
        self.canton.save()
        self.valid_data = {
            "total": "0",
            "active": "0",
            "notActive": "0",
            "totalObjects": "0",
            "totalSubjects": "0",
        }

    def test_if_queryisnone(self):
        response = self.client.get(self._URL_)
        self.assertEqual(response.status_code, 400)

    def test_if_query_district(self):
        response = self.client.get(self._URL_, {"district": self.canton.district_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.valid_data)

    def test_if_query_conton(self):
        response = self.client.get(self._URL_, {"conton": self.canton.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.valid_data)

    def test_if_query_all(self):
        response = self.client.get(
            self._URL_, {"conton": self.canton.id, "district": self.canton.district_id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.valid_data)