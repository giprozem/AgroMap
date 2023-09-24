from rest_framework.test import APITestCase, APIClient

from gip.tests.factories import ContourFactory

"""
Test cases related to Contour statistics.
"""


class ContourStatisticTestCase(APITestCase):
    """
    Sets up a single contour instance before each test.
    """

    _URL_ = "/veg/contour-veg-index-statistics/"

    def setUp(self) -> None:
        contour = ContourFactory()
        self.contour = contour

    """
    Tests that a 500 status code (internal server error) is returned when no data is sent to the endpoint.
    """

    def test_if_dataisnone(self):
        self.client = APIClient(raise_request_exception=False)
        response = self.client.get(self._URL_)
        self.assertEqual(response.status_code, 500)

    """
    Tests if the endpoint returns a successful 200 status code when provided with a start and end date.
    """

    def test_ifData(self):
        response = self.client.get(self._URL_, {"start": "2023-08-15", "end": "2023-08-16"})
        self.assertEqual(response.status_code, 200)
