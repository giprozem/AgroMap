# Required imports for Django Rest Framework testing
from rest_framework.test import APITestCase

# Import required models
from hub.models.land_info import LandInfo
from account.models.account import MyUser


class ZemBalanceViewSetTestCase(APITestCase):
    # URL endpoint that will be tested
    _URL_ = "/hub/zem_balance/"

    # Helper method to construct the request data for land creation
    def _method_create(self):
        request_data = {
            "ink_code": "test_ink_code_1",
            "main_map": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [74.398127, 42.855267],
                        [74.398127, 42.864264],
                        [74.414692, 42.864264],
                        [74.414692, 42.855267],
                        [74.398127, 42.855267],
                    ]
                ],
            },
        }

        return request_data

    # Helper method to create a test user for authentication purposes
    def _create_user(self):
        user = MyUser(username="test_username", is_active=True)
        user.set_password("test_password")
        user.save()
        self.user = user

    # Helper method to create a type of land instance for testing purposes
    def _create_land_type(self):
        land_info = LandInfo(ink_code="test_ink_code")
        land_info.save()
        self.land_info = land_info

    # Setup method to prepare the test environment
    # This is executed before each individual test method in this class
    def setUp(self):
        self._create_user()  # Create a user for the test
        self._create_land_type()  # Create a land type for the test
        self.client.force_authenticate(self.user)  # Authenticate the test user

    # Test method to ensure a GET request to the endpoint returns a 200 status code
    def test_status_code_200(self):
        response = self.client.get(self._URL_)  # Perform a GET request
        self.assertEqual(response.status_code, 200)  # Check if the response code is 200
