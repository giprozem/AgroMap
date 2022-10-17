from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from django.contrib.auth import get_user_model
from plot.models import Plot, CultureField
from .factories import CultureFieldFactory


User = get_user_model()


class CultureTests(APITestCase):
    def setUp(self):
        new_user = User.objects.create(username="test_user_1")
        plot = Plot.objects.create(user=new_user)
        culture_fields = CultureField.objects.bulk_create([
            CultureField(plot=plot, what="cucumber", start="2022-05-15", end="2022-09-21"),
            CultureField(plot=plot, what="malina", start="2022-06-29")
        ])

        self.user = new_user
        self.plot = plot
        self.culture_fields = culture_fields

    def test_get_culture_fields_by_user_success_200(self):
        c1 = self.culture_fields[0]
        c2 = self.culture_fields[1]
        expected_data = [
            {
                "id": c1.id,
                "what": c1.what,
                "start": c1.start,
                "end": c1.end,
                "geometry": None,
                "plot": self.plot.id,
                "crops": []
            },
            {
                "id": c2.id,
                "what": c2.what,
                "start": c2.start,
                "end": None,
                "geometry": None,
                "plot": self.plot.id,
                "crops": []
            }
        ]

        response = self.client.get(f"/cultures_fields/{self.user.id}/")
        self.assertEqual(response.data, expected_data, f"Данные не совпадают")
        self.assertEqual(response.status_code, HTTP_200_OK)


    def test_create_culture_fields_success_201(self):
        c1 = self.culture_fields[0]
        expected_data = {
                "what": c1.what,
                "start": c1.start,
                "end": c1.end,
                "geometry": '',
                "plot": self.plot.id
            }
        response = self.client.post(f"/cultures_fields/{self.user.id}/", expected_data)
        print(response.data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_get_plots_by_user_success_200(self):
        expected_data = [
            {
                "id": self.plot.id,
                "name": None,
                "region": None,
                "user": self.user.id
            }
        ]

        response = self.client.get(f"/plot/{self.user.id}/")
        self.assertEqual(response.data, expected_data, f"Данные не совпадают")
        self.assertEqual(response.status_code, HTTP_200_OK)


class CultureFactoryTests(APITestCase):
    def test_get_culture_fields_by_user_success_200(self):
        c1 = CultureFieldFactory()
        expected_data = [
            {
                "id": c1.id,
                "what": c1.what,
                "start": c1.start,
                "end": c1.end,
                "geometry": None,
                "plot": c1.plot.id,
                "crops": []
            }
        ]

        response = self.client.get(f"/cultures_fields/{c1.plot.user.id}/")
        self.assertEqual(response.data, expected_data, f"Данные не совпадают")
        self.assertEqual(response.status_code, HTTP_200_OK)


class PlotTest(APITestCase):
    def test_get_plots_by_not_exist_user_should_be_empty(self):
        response = self.client.get(f"/plot/2/")
        self.assertEqual(len(response.data), 0)

