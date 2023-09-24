# Import necessary modules for testing
from rest_framework.test import APITestCase, APIClient
from django.db.models.signals import post_save, pre_save

# Import Factory Boy and Faker for generating test data
import factory
from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

# Import models and factories from the application
from ai.models import Contour_AI
from gip.tests.factories import (
    ContonFactory,
    LandTypeFactory,
    CultureFactory,
    ContourFactory,
    get_polygon,
)


# Define a factory for generating test data for the Contour_AI model
class Contour_AIFactory(DjangoModelFactory):
    conton = SubFactory(ContonFactory)
    polygon = get_polygon()
    year = 2022
    productivity = 1
    type = SubFactory(LandTypeFactory)
    culture = SubFactory(CultureFactory)

    class Meta:
        model = Contour_AI


# Define a test case for querying polygons in a specific screen area
class PolygonsInScreenTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        contour = ContourFactory()
        self.contour = contour

    def test_polygons_get_ifparamsisnone(self):
        # Test if the API returns a 400 Bad Request response when parameters are missing
        response = self.client.post("/gip/polygons-in-screen/")
        self.assertEqual(response.status_code, 400)

    def test_polygon_if_bodyisnone(self):
        # Test if the API returns a 400 Bad Request response when the request body is missing
        landtype_id = self.contour.type_id
        response = self.client.post(f"/gip/polygons-in-screen/?land_type={landtype_id}")
        self.assertEqual(response.status_code, 400)

    def test_polygon_get_ifparams(self):
        # Test if the API returns a 200 OK response when valid parameters are provided
        request_data = {
            "_southWest": {"lat": 38, "lng": 44.38859908922761},
            "_northEast": {"lat": 69.71093250783867, "lng": 80.4042846475467},
        }
        landtype_id = self.contour.type_id
        response = self.client.post(
            f"/gip/polygons-in-screen/?land_type={landtype_id}",
            request_data,
            format="json",
        )
        self.assertEqual(response.status_code, 200)


# Define a test case for filtering contours
class FilterContourApiTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        self.client = APIClient(raise_request_exception=False)
        contour = ContourFactory()
        self.contour = contour

    def test_contour_search_if_params(self):
        # Test if the API returns a 200 OK response when valid search parameters are provided
        ink = self.contour.ink
        response = self.client.get(f"/gip/contour-search/?search={ink}")
        self.assertEqual(response.status_code, 200)

    def test_contour_search_if_paramsisnone(self):
        # Test if the API returns a 200 OK response when no search parameters are provided
        response = self.client.get(f"/gip/contour-search/")
        self.assertEqual(response.status_code, 200)

    def test_contour_search_notresult(self):
        # Test if the API returns a 200 OK response when no results are found for the search
        ink = "invalid_ink"
        response = self.client.get(f"/gip/contour-search/?search={ink}")
        self.assertEqual(response.status_code, 200)


# Define a test case for querying coordinates of a polygon
class CoordinatesPolygonTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        contour = ContourFactory()
        self.region = contour.conton.district.region_id
        self.district = contour.conton.district_id
        self.conton = contour.conton_id
        self.client = APIClient(raise_request_exception=False)

    def test_coords_ifparamsall(self):
        # Test if the API returns a 500 Internal Server Error response when providing all parameters
        response = self.client.get(
            f"/gip/coordinates-polygon/?region={self.region}&district={self.district}&conton={self.conton}/"
        )
        self.assertEqual(response.status_code, 500)  # TODO api not working correct

    def test_coords_ifparamsconton(self):
        # Test if the API returns a 500 Internal Server Error response when providing only the 'conton' parameter
        response = self.client.get(f"/gip/coordinates-polygon/?conton={self.conton}/")
        self.assertEqual(response.status_code, 500)  # TODO api not working correct

    def test_coords_ifparamsdistrict(self):
        response = self.client.get(
            f"/gip/coordinates-polygon/?district={self.district}/"
        )
        self.assertEqual(response.status_code, 500)  # TODO api not working correct

    def test_coords_ifparamsregion(self):
        response = self.client.get(f"/gip/coordinates-polygon/?region={self.region}/")
        self.assertEqual(response.status_code, 500)  # TODO api not working correct

    def test_coords_ifparams_isnone(self):
        response = self.client.get(f"/gip/coordinates-polygon/")
        self.assertEqual(response.status_code, 200)


# Define a factory for generating test data for the Contour_AI model
class Contour_AIFactory(DjangoModelFactory):
    conton = SubFactory(ContonFactory)
    polygon = get_polygon()
    year = 2022
    productivity = 1
    type = SubFactory(LandTypeFactory)
    culture = SubFactory(CultureFactory)

    class Meta:
        model = Contour_AI


# Define a test case for querying contour productivity on a map
class ContourProductivityTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        contour = ContourFactory()
        self.region = contour.conton.district.region_id
        self.district = contour.conton.district_id
        self.conton = contour.conton_id
        self.year = contour.year
        self.ink = contour.year
        self.land_type = contour.type_id
        self.culture = contour.culture_id
        self.client = APIClient(raise_request_exception=False)

    def test_mapcontour_ifparamsall(self):
        # Test if the API returns a 200 OK response when providing all parameters
        response = self.client.get(
            f"/gip/contour-map-productivity/?region={self.region}&district={self.district}&conton={self.conton}&year={self.year}&land_type={self.land_type}"
        )
        self.assertEqual(response.status_code, 200)

    def test_mapcontour_ifparamsisnone(self):
        # Test if the API returns a 400 Bad Request response when parameters are missing
        response = self.client.get(f"/gip/contour-map-productivity/")
        self.assertEqual(response.status_code, 400)

    def test_statistic_contour_ifparamsisnone(self):
        # Test if the API returns a 400 Bad Request response when parameters are missing
        response = self.client.get("/gip/contour-statistics-productivity/")
        self.assertEqual(response.status_code, 400)

    def test_statistic_contour_ifparams(self):
        # Test if the API returns a 200 OK response when valid parameters are provided
        response = self.client.get(
            f"/gip/contour-statistics-productivity/?year={self.year}&land_type={self.land_type}&region={self.region}&district={self.district}&conton={self.conton}"
        )
        self.assertEqual(response.status_code, 200)


# Define a test case for culture statistics
class CultureStatisticsTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        ai = Contour_AIFactory()
        self.ai = ai
        self.land_type = self.ai.type_id
        self.culture = self.ai.culture_id
        self.region = self.ai.conton.district.region_id
        self.conton = self.ai.conton_id
        self.district = self.ai.conton.district_id

    def test_culture_statistic_ifqueryisnone(self):
        # Test if the API returns a 400 Bad Request response when parameters are missing
        response = self.client.get("/gip/culture-statistics/")
        self.assertEqual(response.status_code, 400)

    def test_culture_statistic_ifquery(self):
        # Test if the API returns a 200 OK response when valid parameters are provided
        response = self.client.get(
            f"/gip/culture-statistics/?year={self.ai.year}&land_type={self.land_type}"
        )
        self.assertEqual(response.status_code, 200)

    def test_culture_statistic_ifqueryall(self):
        # Test if the API returns a 200 OK response when providing all parameters
        response = self.client.get(
            f"/gip/culture-statistics/?year={self.ai.year}&land_type={self.land_type}&ai={self.ai.id}&culture={self.culture}&district={self.district}&region={self.region}"
        )
        self.assertEqual(response.status_code, 200)


# Define a test case for contour statistics
class ContourStatisticsTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        contour = ContourFactory()
        self.region = contour.conton.district.region_id
        self.district = contour.conton.district_id
        self.conton = contour.conton_id
        self.year = contour.year
        self.ink = contour.year
        self.land_type = contour.type_id
        self.culture = contour.culture_id
        self.client = APIClient(raise_request_exception=False)

    def test_contourstatistic_ifqueryisnone(self):
        # Test if the API returns a 400 Bad Request response when parameters are missing
        response = self.client.get("/gip/contour-statistics/")
        self.assertEqual(response.status_code, 400)

    def test_contourstatistic_ifquery(self):
        # Test if the API returns a 200 OK response when valid parameters are provided
        response = self.client.get(
            f"/gip/contour-statistics/?region={self.region}&culture={self.culture}"
        )
        self.assertEqual(response.status_code, 200)


# Define a test case for filtering contours
class FilterContourTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        ai = Contour_AIFactory()
        self.ai = ai
        self.land_type = self.ai.type_id
        self.culture = self.ai.culture_id
        self.region = self.ai.conton.district.region_id
        self.conton = self.ai.conton_id
        self.district = self.ai.conton.district_id

    def test_filter_contour_ifqueryisnone(self):
        # Test if the API returns a 400 Bad Request response when parameters are missing
        response = self.client.get("/gip/filter_contour/")
        self.assertEqual(response.status_code, 400)

    def test_filter_contour_ifquery(self):
        # Test if the API returns a 200 OK response when valid parameters are provided
        self.client = APIClient(raise_request_exception=False)
        response = self.client.get(
            f"/gip/filter_contour/?land_type={self.land_type}&year={self.ai.year}"
        )
        self.assertEqual(response.status_code, 200)

    def test_filter_contour_ifqueryall(self):
        # Test if the API returns a 200 OK response when providing all parameters
        self.client = APIClient(raise_request_exception=False)
        response = self.client.get(
            f"/gip/filter_contour/?land_type={self.land_type}&year={self.ai.year}&region={self.region}&district={self.district}&ai={self.ai.id}&conton={self.conton}&culture={self.culture}"
        )
        self.assertEqual(response.status_code, 200)


class PolygonsInBboxTestCase(APITestCase):
    url = "polygons-in-bbox/"

    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        contour = ContonFactory()
        self.contour = contour
        self.min_long = Faker().pyfloat(
            right_digits=4, positive=True, min_value=71, max_value=74
        )
        self.max_long = Faker().pyfloat(
            right_digits=4, positive=True, min_value=75, max_value=78
        )

        self.min_lat = Faker().pyfloat(
            right_digits=4, positive=True, min_value=38, max_value=39
        )
        self.max_lat = Faker().pyfloat(
            right_digits=4, positive=True, min_value=40, max_value=44
        )

    def test_polygoninbox_ifparamsisnone(self):
        # Test if the API returns a 400 Bad Request response when parameters are missing
        response = self.client.get("/gip/polygons-in-bbox/")
        self.assertEqual(response.status_code, 400)


# Define a test case for culture percentage statistics
class CulturePercentTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        contour = ContourFactory()
        self.region = contour.conton.district.region_id
        self.district = contour.conton.district_id
        self.conton = contour.conton_id
        self.year = contour.year
        self.ink = contour.year
        self.land_type = contour.type_id
        self.culture = contour.culture_id
        self.client = APIClient(raise_request_exception=False)

    def test_culture_stats_ifparamsisnone(self):
        # Test if the API returns a 400 Bad Request response when parameters are missing
        response = self.client.get("/gip/culture-percent/")
        self.assertEqual(response.status_code, 400)

    def test_culture_stats_ifparams(self):
        # Test if the API returns a 200 OK response when valid parameters are provided
        response = self.client.get(f"/gip/culture-percent/?year=2022")
        self.assertEqual(response.status_code, 200)

    def test_culture_stats_ifparamsall(self):
        # Test if the API returns a 200 OK response when providing all parameters
        response = self.client.get(
            f"/gip/culture-percent/?year={self.year}&region={self.region}&district={self.district}"
        )
        self.assertEqual(response.status_code, 200)


# Define a test case for graphic tables
class GraphicTablesTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        contour = ContourFactory()
        self.region = contour.conton.district.region_id
        self.district = contour.conton.district_id
        self.conton = contour.conton_id
        self.year = contour.year
        self.ink = contour.year
        self.land_type = contour.type_id
        self.culture = contour.culture_id
        self.client = APIClient(raise_request_exception=False)

    def test_graphic_if_queryisnone(self):
        # Test if the API returns a 400 Bad Request response when parameters are missing
        response = self.client.get("/gip/graphic-tables/")
        self.assertEqual(response.status_code, 400)

    def test_graphic_if_query(self):
        # Test if the API returns a 200 OK response when valid parameters are provided
        response = self.client.get(f"/gip/graphic-tables/?culture={self.culture}")
        self.assertEqual(response.status_code, 200)


# Define a test case for occurrence checks
class OccurrenceCheckTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        self.contour = ContourFactory()

    def test_occurence_ifparamsisnone(self):
        # Test if the API returns a 400 Bad Request response when parameters are missing
        response = self.client.get("/gip/occurrence-check/")
        self.assertEqual(response.status_code, 400)

    def test_occurence_ifparams_point(self):
        # Test if the API returns a 200 OK response when valid parameters are provided
        response = self.client.get(f"/gip/occurrence-check/?point=37.1234,55.6789")
        self.assertEqual(response.status_code, 200)
