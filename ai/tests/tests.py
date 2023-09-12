import factory

from rest_framework.test import APITestCase, APIClient
from django.db.models.signals import post_save, pre_save

from gip.tests.test_additional_views import Contour_AIFactory
from account.tests.factories import AdminTokenFactory, TokenFactory
from ai.tests.factories import (
    ProcessFactory,
    PredictedContourVegIndexFactory,
    CreateDescriptionFactory,
)

from account.tests.factories import AdminTokenFactory
from ai.tests.factories import ProcessFactory


class AiSearchTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        process = ProcessFactory(id=1)
        self.process = process
        self.token = AdminTokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_if_process_isrunning(self):
        response = self.client.get("/ai/search-contour/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message")["en"], "The process is underway")

    def test_if_process_isstopped(self):
        self.process.is_running = False
        response = self.client.get("/ai/search-contour/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message")["en"], "The process is underway")


class Contour_AIInScreenTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        self.contour_ai = Contour_AIFactory()
        self.year = self.contour_ai.year
        self.culture = self.contour_ai.culture_id
        self.request_data = {
            "_southWest": {"lat": 42.70399473713915, "lng": 78.38859908922761},
            "_northEast": {"lat": 42.71093250783867, "lng": 78.4042846475467},
        }

    def test_contour_in_screen_with_requestbody(self):
        response = self.client.post(
            "/ai/contour-in-screen/", self.request_data, format="json"
        )
        self.assertEqual(response.status_code, 200)

    def test_contour_in_screen_with_requestbody_year(self):
        response = self.client.post(
            f"/ai/contour-in-screen/?year={self.year}", self.request_data, format="json"
        )
        self.assertEqual(response.status_code, 200)

    def test_contour_in_screen_with_requestbody_culture(self):
        response = self.client.post(
            f"/ai/contour-in-screen/?year={self.year}&culture={self.culture}",
            self.request_data,
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_contour_in_screen_without_requestbody(self):
        response = self.client.post("/ai/contour-in-screen/")
        self.assertEqual(response.status_code, 400)


class CreateDatasetTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        process = ProcessFactory(id=1)
        self.process = process
        self.token = AdminTokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_dataset_ifproccess(self):
        self.process.is_running = True
        response = self.client.get("/ai/create-dataset/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message")["en"], "The process is underway")

    def test_create_dataset_ifprocess_false(self):
        self.process.is_running = False
        response = self.client.get("/ai/create-dataset/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message")["en"], "The process is underway")


class ContourAiTestCase(APITestCase):
    _URL_ = "/ai/contour/"

    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        self.contour = Contour_AIFactory()
        self.token = AdminTokenFactory()
        self.client = APIClient(raise_request_exception=False)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_contour_viewset_get(self):
        response = self.client.get(self._URL_)
        self.assertEqual(response.status_code, 200)

    def test_contour_viewset_update(self):
        updated_data = {
            "year": "2023",
            "productivity": 10,
        }
        response = self.client.patch(
            self._URL_ + f"{self.contour.id}/", updated_data, format="json"
        )
        if updated_data.get("polygon") is None:
            self.assertEqual(response.status_code, 500)
        else:
            self.assertEqual(response.status_code, 200)

    def test_contour_viewset_destroy_if_useradmin(self):
        response = self.client.delete(self._URL_ + f"{self.contour.id}/")
        self.assertEqual(response.status_code, 200)

    def test_contout_viewset_destroy_if_user(self):
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(self._URL_ + f"{self.contour.id}/")
        self.assertEqual(response.status_code, 403)


class PivotTableTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        self.ai_contour = Contour_AIFactory()
        self.culture_id = self.ai_contour.culture_id

    def test_if_params_isnone(self):
        response = self.client.get("/ai/pivot_table_culture/")
        self.assertEqual(response.status_code, 400)

    def test_if_params(self):
        response = self.client.get(
            f"/ai/pivot_table_culture/?culture={self.culture_id}"
        )
        self.assertEqual(response.status_code, 200)


class PredictContourTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        self.index = PredictedContourVegIndexFactory()

    def test_if_date_isnot_correct(self):
        response = self.client.get("/ai/predict-productivity/")
        self.assertEqual(response.status_code, 200)

    def test_if_date_is_correct(self):
        self.index.date = "2022-06-21"
        response = self.client.get("/ai/predict-productivity/")
        self.assertEqual(response.status_code, 200)


class CreateDescriptionTestCase(APITestCase):
    @factory.django.mute_signals(pre_save, post_save)
    def setUp(self) -> None:
        self.create_description_model = CreateDescriptionFactory()

    def test_create_description_user_request(self):
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/ai/instruction/")
        self.assertEqual(response.status_code, 403)

    def test_create_description_admin_user_request(self):
        self.token = AdminTokenFactory()
        self.client = APIClient(raise_request_exception=False)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/ai/instruction/")
        self.assertEqual(response.status_code, 200)


class CleanContourCreateTestCase(APITestCase):
    def test_get(self):
        response = self.client.get("/ai/clean/")
        self.assertEqual(response.status_code, 200)
