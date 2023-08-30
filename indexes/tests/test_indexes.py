import json

from rest_framework.test import APITestCase, APIClient
from django.contrib.gis.geos import GEOSGeometry

from indexes.models.actual_veg_index import ActualVegIndex, PredictedContourVegIndex
from culture_model.models.vegetation_index import VegetationIndex
from ai.models import Contour_AI

from gip.tests.factories import ContourFactory, ContonFactory


class ActualVegIndexTestCase(APITestCase):
    _URL_ = "/veg/actual-veg-indexes/"

    def setUp(self) -> None:
        contour = ContourFactory()
        veg_index = VegetationIndex(
            name="test_veg_index", description="test_veg_index_description"
        )
        veg_index.save()
        actual_index = ActualVegIndex(
            average_value=1.0, index=veg_index, contour=contour, date="2023-01-01"
        )
        actual_index.save()

    def test_actual_indexes_view_if_query(self):
        response = self.client.get(self._URL_, {"contour_id": 1})
        self.assertEqual(response.status_code, 204)

    def test_actual_indexes_view_if_queryisnone(self):

        self.client = APIClient(raise_request_exception=False)
        response = self.client.get(self._URL_)
        self.assertEqual(response.status_code, 500)



class PredictedContourVegIndexTestCase(APITestCase):
    _URL_ = "/veg/ai-actual-veg-indexes/"

    geometry_field ={
            "type": "Polygon",
            "coordinates": [
                [
                    [74.398127, 42.855267],
                    [74.398127, 42.864264],
                    [74.414692, 42.864264],
                    [74.414692, 42.855267],
                    [74.398127, 42.855267],
                ]
            ]}

    def setUp(self) -> None:
        polygon_wkt = json.dumps(self.geometry_field)
        polygon_field = GEOSGeometry(polygon_wkt)
        conton = ContonFactory()
        index = VegetationIndex.objects.create(
            name="test_veg_index", description="test_veg_index_description"
        )
        contour_ai = Contour_AI.objects.create(conton=conton, polygon=polygon_field)

        pc_veg_index = PredictedContourVegIndex(
            average_value=10.10, contour=contour_ai, index=index, date="2023-01-01"
        )
        pc_veg_index.save()

    def test_actual_index_ai_ifcontour_inquery(self):
        response = self.client.get(self._URL_, {"contour_id": 1})
        self.assertEqual(response.status_code, 200)

    def test_ai_satellite_dates(self):
        
        url = f"/veg/ai-satellite_dates/1/1/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) #TODO need to add assert valid data and response data

    def test_satellite_dates(self):
        url = "/veg/satellite_dates/1/1/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
