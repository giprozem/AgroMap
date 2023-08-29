import json

from rest_framework.test import APITestCase

from hub.models.land_info import LandInfo

from account.models.account import MyUser


class ZemBalanceViewSetTestCase(APITestCase):
    _URL_ = "/hub/zem_balance/"

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

    def _create_user(self):
        user = MyUser(username="test_username", is_active=True)
        user.set_password("test_password")
        user.save()
        self.user = user

    def _create_land_type(self):
        land_info = LandInfo(ink_code="test_ink_code")
        land_info.save()
        self.land_info = land_info

    def setUp(self):
        self._create_user()
        self._create_land_type()
        self.client.force_authenticate(self.user)

    def test_status_code_200(self):
        response = self.client.get(self._URL_)
        self.assertEqual(response.status_code, 200)
