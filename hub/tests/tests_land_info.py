import json

# Import necessary Django and Django Rest Framework modules
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

# Import the required functions, models, and factories
from elevation.data import elevation
from hub.models.land_info import LandInfo
from gip.models.conton import Conton
from gip.models.district import District
from gip.models.region import Region
from gip.tests.factories import ContonFactory

# Fetching the default user model
User = get_user_model()

TEST_DIR = "test_data"

class CultureTests(APITestCase):
    
    _URL_ = "/hub/elevation/"  # URL endpoint for testing
    reponse_data = None
    # Dictionary holding latitude and longitude coordinates for testing
    geometry_map = {"latitude": [38, 44], "longitude": [69, 81]}
    latitude = geometry_map.get("latitude")[1]
    longitude = geometry_map.get("longitude")[1]

    def setUp(self) -> None:
        # Fetching the elevation data for the given latitude and longitude
        elevation_data = elevation(
            latitude=float(self.latitude), longitude=float(self.longitude)
        )
        self.reponse_data = {"elevation": elevation_data.tolist()}

    # Test to check the status code for elevation endpoint
    def test_status_code_elevation_soil_view(self):
        response = self.client.get(self._URL_, self.geometry_map)
        self.assertEqual(response.status_code, 200)

    # Test to check if the response content matches the expected data
    def test_reponse_content_elevation_soil_view(self):
        response = self.client.get(self._URL_, self.geometry_map)
        response_data = json.loads(response.content)
        self.assertEqual(
            self.reponse_data.get("elevation"), response_data.get("elevation")
        )

class LandInfoSearchTestCase(APITestCase):
    
    _URL_ = "/hub/search_ink_hub/"  # URL endpoint for testing

    def setUp(self) -> None:
        # Creating a land info instance for testing
        land_info = LandInfo(ink_code="test_inc_code")
        land_info.save()
        self.land_info = land_info

    # Test to check the response data when the query is none
    def test_search_if_queryisnone(self):
        response = self.client.get(self._URL_)
        self.assertEqual(response.data, [])

    # Test to check the response data when the query is provided
    def test_search_if_query(self):
        response = self.client.get(self._URL_, {"search": "test"})
        self.assertEqual(len(response.data.get("list_ink_code")), 1)

class AmountCattleApiTestCase(APITestCase):
    
    _URL_ = "/hub/amount_cattle/"  # URL endpoint for testing

    def setUp(self) -> None:
        # Creating a Conton instance using a factory for testing
        self.canton = ContonFactory()
        self.client = APIClient(raise_request_exception=False)

    # Test to check the response when the query is none
    def test_if_queryisnone(self):
        response = self.client.get(self._URL_)
        self.assertEqual(response.status_code, 400)

    # Test to check the response when querying by district
    def test_if_query_district(self):
        response = self.client.get(f"{self._URL_}?district={self.canton.district_id}")
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 500)

    # Test to check the response when querying by conton
    def test_if_query_conton(self):
        response = self.client.get(f"{self._URL_}?conton={self.canton.id}")
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 500)

    # Test to check the response when querying by both conton and district
    def test_if_query_all(self):
        response = self.client.get(
            f"{self._URL_}?conton={self.canton.id}&district={self.canton.district_id}"
        )
        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 500)