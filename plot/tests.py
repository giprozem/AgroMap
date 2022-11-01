from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from django.contrib.auth import get_user_model
from plot.models import Plot, CultureField, Crop
from .factories import CultureFieldFactory, CropFactory, SoilAnalysisFactory
from django.test import override_settings


User = get_user_model()

TEST_DIR = 'test_data'


class CultureTests(APITestCase):
    def setUp(self):
        new_user = User.objects.create(username="test_user_1")
        plot = Plot.objects.create(user=new_user)
        culture_fields = CultureField.objects.bulk_create([
            CultureField(plot=plot, what="cucumber", start="2022-05-15", end="2022-09-21"),
            CultureField(plot=plot, what="cucumber", start="2022-05-15", end="2022-09-21")
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
                "end": c2.end,
                "geometry": None,
                "plot": self.plot.id,
                "crops": []
            }
        ]
        response = self.client.get(f"/cultures_fields/{self.user.id}/")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data, 'Dannye ne sovpadaut')

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
    def setUp(self):
        new_user = User.objects.create(username="test_user_1")
        plot = Plot.objects.bulk_create([
            Plot(name='plot_1', region='Chui'),
            Plot(name='plot_2', region='Naryn')
        ])

        self.user = new_user
        self.plot = plot

    def test_get_plots_by_not_exist_user_should_be_empty(self):
        response = self.client.get(f"/plot/2/")
        self.assertEqual(len(response.data), 0)

    def test_create_plot_success_201(self):
        p1 = self.plot[0]
        expected_data = {
            "user": self.user.id,
            "name": p1.name,
            "region": p1.region
        }

        response = self.client.post(f"/plots/", expected_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_update_plot_success_200(self):
        p1 = self.plot[0]
        expected_data = {
            "user": self.user.id,
            "name": "test_name",
            "region": "test_region",
        }
        response = self.client.put(f"/plots/{p1.id}/", expected_data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_delete_plot_200(self):
        p1 = self.plot[0]
        response = self.client.delete(f"/plots/{p1.id}/")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)


class CropTest(APITestCase):
    def setUp(self):
        new_user = User.objects.create(username="test_user_1")
        plot = Plot.objects.create(user=new_user)
        culture_fields = CultureField.objects.create(plot=plot, what="cucumber", start="2020-05-15", end="2024-09-21")
        crops = Crop.objects.bulk_create([
            Crop(culture=culture_fields, what='crops_what_1', quantity=1234, unit='kg', start='2021-01-23'),
            Crop(culture=culture_fields, what='crops_what_2', quantity=6543, unit='l', start='2022-01-23', end='2026-01-01')
        ])

        self.user = new_user
        self.plot = plot
        self.culture_fields = culture_fields
        self.crops = crops

    def test_get_crop_success_200(self):
        c1 = self.crops[0]
        c2 = self.crops[1]
        expected_data = [
            {
                "id": c1.id,
                "what": c1.what,
                "quantity": c1.quantity,
                "unit": c1.unit,
                "start": c1.start,
                "end": None,
                "culture": c1.culture
            },
            {
                "id": c2.id,
                "what": c2.what,
                "quantity": c2.quantity,
                "unit": c2.unit,
                "start": c2.start,
                "end": c2.end,
                "culture": c2.culture
            }
        ]

        response = self.client.get(f"/crop/")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_crop_success_201(self):
        c1 = CropFactory()
        expected_data = {
            "what": c1.what,
            "quantity": 322,
            "unit": c1.unit,
            "start": "2021-01-07",
            "end": "",
            "culture": c1.culture.id
        }
        response = self.client.post(f"/crop/", expected_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_update_crop_success_200(self):
        c1 = CropFactory()

        expected_data = {
            "culture": c1.culture.id,
            "what": "test_what_crop",
            "quantity": 342,
            "unit": 'LL',
            "start": '2021-09-09',
            "end": ""
        }

        response = self.client.put(f"/crop/{c1.id}/", expected_data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_delete_crop_success_200(self):
        c1 = CropFactory()

        response = self.client.delete(f"/crop/{c1.id}/")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)


class SoilAnalysisTest(APITestCase):

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_get_soil_analysis_success_200(self):
        s1 = SoilAnalysisFactory()
        response = self.client.get(f"/soil-analysis/{s1.id}/")
        self.assertEqual(response.status_code, HTTP_200_OK)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_create_soil_analysis_success_201(self):
        s1 = SoilAnalysisFactory()
        expected_data = {
            "photo": s1.photo,
            "date": s1.date,
            "description": s1.description,
            "culture_field": s1.culture_field.id

        }
        response = self.client.post(f"/soil-analysis/", expected_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_updated_soil_analysis_success_201(self):
        s1 = SoilAnalysisFactory()
        expected_data = {
            "photo": s1.photo,
            "date": s1.date,
            "description": s1.description,
            "culture_field": s1.culture_field.id

        }
        response = self.client.put(f"/soil-analysis/{s1.id}/", expected_data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_deleted_soil_analysis_success_204(self):
        s1 = SoilAnalysisFactory()
        response = self.client.delete(f"/soil-analysis/{s1.id}/")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
