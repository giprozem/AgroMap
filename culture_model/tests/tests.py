# Import necessary modules and classes
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase
from culture_model.tests.factories import VegetationIndexFactory

# Create a test case class named TestCulture that inherits from APITestCase
class TestCulture(APITestCase):

    # Define a test method named test_index
    def test_index(self):
        # Test the endpoint '/info/index-list/' when there are no records (expecting HTTP_400_BAD_REQUEST)
        response = self.client.get('/info/index-list/')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        # Create a VegetationIndex instance using the factory
        veg = VegetationIndexFactory()

        # Test the endpoint '/info/index-list/' after creating a record (expecting HTTP_200_OK)
        response = self.client.get('/info/index-list/')
        self.assertEqual(response.status_code, HTTP_200_OK)

        # Define the expected data based on the created VegetationIndex instance
        expected_data = [
            {
                "id": veg.id,
                "name_ru": veg.name,
                "name_ky": None,
                "name_en": None,
                "description_ru": veg.description,
                "description_ky": None,
                "description_en": None
            }
        ]

        # Assert that the response data matches the expected data
        self.assertEqual(response.data, expected_data)
