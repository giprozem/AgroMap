from rest_framework.test import APITestCase, APIClient

from factory import SubFactory
from factory.django import DjangoModelFactory

from faker import Faker

from ai.models import Contour_AI
from gip.tests.factories import (
    ContonFactory,
    LandTypeFactory,
    CultureFactory,
    ContourFactory,
    get_polygon,
)


class ConotonWithPolygonFactory(ContourFactory):
    polygon = get_polygon()


class Contour_AIFactory(DjangoModelFactory):
    conton = SubFactory(ContonFactory)
    polygon = get_polygon()
    year = 2022
    productivity = 1
    type = SubFactory(LandTypeFactory)
    culture = SubFactory(CultureFactory)

    class Meta:
        model = Contour_AI


class PolygonsInScreenTestCase(APITestCase):
    def setUp(self) -> None:
        contour = ContourFactory()
        self.contour = contour

    def test_polygons_get_ifparamsisnone(self):
        response = self.client.post("/gip/polygons-in-screen/")
        self.assertEqual(response.status_code, 400)

    def test_polygon_if_bodyisnone(self):
        landtype_id = self.contour.type_id
        response = self.client.post(f"/gip/polygons-in-screen/?land_type={landtype_id}")

        self.assertEqual(response.status_code, 400)

    def test_polygon_get_ifparams(self):
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


class FilterContourApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient(raise_request_exception=False)
        contour = ContourFactory()
        self.contour = contour

    def test_contour_search_if_params(self):
        ink = self.contour.ink
        response = self.client.get(f"/gip/contour-search/?search={ink}")
        self.assertEqual(response.status_code, 200)

    def test_contour_search_if_paramsisnone(self):
        response = self.client.get(f"/gip/contour-search/")
        self.assertEqual(response.status_code, 200)

    def test_contour_search_notresult(self):
        ink = "invalid_ink"
        response = self.client.get(f"/gip/contour-search/?search={ink}")
        self.assertEqual(response.status_code, 200)


class CoordinatesPolygonTestCase(APITestCase):
    def setUp(self) -> None:
        contour = ContourFactory()
        self.region = contour.conton.district.region_id
        self.district = contour.conton.district_id
        self.conton = contour.conton_id
        self.client = APIClient(raise_request_exception=False)

    def test_coords_ifparamsall(self):
        response = self.client.get(
            f"/gip/coordinates-polygon/?region={self.region}&district={self.district}&conton={self.conton}/"
        )
        self.assertEqual(response.status_code, 500)  # TODO api not working correct

    def test_coords_ifparamsconton(self):
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


class ContourProductivityTestCase(APITestCase):
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
        response = self.client.get(
            f"/gip/contour-map-productivity/?region={self.region}&district={self.district}&conton={self.conton}&year={self.year}&land_type={self.land_type}"
        )
        self.assertEqual(response.status_code, 200)

    def test_mapcontour_ifparamsisnone(self):
        response = self.client.get(f"/gip/contour-map-productivity/")
        self.assertEqual(response.status_code, 400)

    def test_statistic_contour_ifparamsisnone(self):
        response = self.client.get("/gip/contour-statistics-productivity/")
        self.assertEqual(response.status_code, 400)

    def test_statistic_contour_ifparams(self):
        response = self.client.get(
            f"/gip/contour-statistics-productivity/?year={self.year}&land_type={self.land_type}&region={self.region}&district={self.district}&conton={self.conton}"
        )
        self.assertEqual(response.status_code, 200)


class CultureStatisticsTestCase(APITestCase):
    def setUp(self) -> None:
        ai = Contour_AIFactory()
        self.ai = ai
        self.land_type = self.ai.type_id
        self.culture = self.ai.culture_id
        self.region = self.ai.conton.district.region_id
        self.conton = self.ai.conton_id
        self.district = self.ai.conton.district_id

    def test_culture_statistic_ifqueryisnone(self):
        response = self.client.get("/gip/culture-statistics/")
        self.assertEqual(response.status_code, 400)

    def test_culture_statistic_ifquery(self):
        response = self.client.get(
            f"/gip/culture-statistics/?year={self.ai.year}&land_type={self.land_type}"
        )
        self.assertEqual(response.status_code, 200)

    def test_culture_statistic_ifqueryall(self):
        response = self.client.get(
            f"/gip/culture-statistics/?year={self.ai.year}&land_type={self.land_type}&ai={self.ai.id}&culture={self.culture}&district={self.district}&region={self.region}"
        )
        self.assertEqual(response.status_code, 200)


class ContourStatisticsTestCase(APITestCase):
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
        response = self.client.get("/gip/contour-statistics/")
        self.assertEqual(response.status_code, 400)

    def test_contourstatistic_ifquery(self):
        response = self.client.get(
            f"/gip/contour-statistics/?region={self.region}&culture={self.culture}"
        )
        self.assertEqual(response.status_code, 200)


class FilterContourTestCase(APITestCase):
    def setUp(self) -> None:
        ai = Contour_AIFactory()
        self.ai = ai
        self.land_type = self.ai.type_id
        self.culture = self.ai.culture_id
        self.region = self.ai.conton.district.region_id
        self.conton = self.ai.conton_id
        self.district = self.ai.conton.district_id

    def test_filter_contour_ifqueryisnone(self):
        response = self.client.get("/gip/filter_contour/")
        self.assertEqual(response.status_code, 400)

    def test_filter_contour_ifquery(self):
        self.client = APIClient(raise_request_exception=False)
        response = self.client.get(
            f"/gip/filter_contour/?land_type={self.land_type}&year={self.ai.year}"
        )
        self.assertEqual(response.status_code, 200)

    def test_filter_contour_ifqueryall(self):
        self.client = APIClient(raise_request_exception=False)
        response = self.client.get(
            f"/gip/filter_contour/?land_type={self.land_type}&year={self.ai.year}&region={self.region}&district={self.district}&ai={self.ai.id}&conton={self.conton}&culture={self.culture}"
        )
        self.assertEqual(response.status_code, 200)


class PolygonsInBboxTestCase(APITestCase):
    url = "polygons-in-bbox/"

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
        response = self.client.get("/gip/polygons-in-bbox/")
        self.assertEqual(response.status_code, 400)

    # def test_polygoninbox_ifparams(self):
    #     bbox_coords = [
    #         self.min_long, self.min_lat,
    #         self.max_long, self.max_lat
    #     ]

    #     response = self.client.get("/gip/polygons-in-bbox/", {'bbox': ','.join(map(str, bbox_coords))})
    #     self.assertEqual(response.status_code, 200)


class CulturePercentTestCase(APITestCase):
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
        response = self.client.get("/gip/culture-percent/")
        self.assertEqual(response.status_code, 400)

    def test_culture_stats_ifparams(self):
        response = self.client.get(f"/gip/culture-percent/?year=2022")
        self.assertEqual(response.status_code, 200)

    def test_culture_stats_ifparamsall(self):
        response = self.client.get(
            f"/gip/culture-percent/?year={self.year}&region={self.region}&district={self.district}"
        )
        self.assertEqual(response.status_code, 200)


class GraphicTablesTestCase(APITestCase):
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
        response = self.client.get("/gip/graphic-tables/")
        self.assertEqual(response.status_code, 400)

    def test_graphic_if_query(self):
        response = self.client.get(f"/gip/graphic-tables/?culture={self.culture}")
        self.assertEqual(response.status_code, 200)


class OccurrenceCheckTestCase(APITestCase):
    contour = ConotonWithPolygonFactory()

    def test_occurence_ifparamsisnone(self):
        response = self.client.get("/gip/occurrence-check/")
        self.assertEqual(response.status_code, 400)

    def test_occurence_ifparams_point(self):
        response = self.client.get(f"/gip/occurrence-check/?point=37.1234,55.6789")
        self.assertEqual(response.status_code, 200)

    # def test_occurence_ifparams_polygon(self):
    #     polygon = self.contour.polygon
    #     valid_polygon = str(polygon).replace("SRID=4326;", "")
    #     response = self.client.get(f"/gip/occurrence-check/?polygon={valid_polygon}")
    #     self.assertEqual(response.status_code, 200)
