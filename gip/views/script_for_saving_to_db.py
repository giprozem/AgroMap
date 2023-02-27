import json
import random

from django.contrib.gis.geos import GEOSGeometry
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import District, Contour, ContourYear
from django.contrib.gis.geos.prototypes.io import wkt_w


class GeojsonSavingToDBAPIView(APIView):
    pass
    # def post(self, request, *args, **kwargs):
    #
    #     with open('kemin_orlovka.geojson') as f:
    #         data = json.load(f)['features']
    #         for i in data:
    #             try:
    #                 uroj = i['properties']['Urojainost']
    #                 uroj = uroj.replace('(', '')
    #                 uroj = uroj.replace(')', '')
    #                 uroj = uroj.replace(',', '.')
    #                 print(uroj)
    #                 polygon = GEOSGeometry(f"{i['geometry']}")
    #                 wkt = wkt_w(dim=2).write(polygon).decode()
    #                 geom = GEOSGeometry(wkt, srid=4326)
    #                 ink = f"{random.randint(400, 500)}-02-123-{random.randint(2000, 9000)}-78-{random.randint(1, 350)}"
    #                 code_soate = f"{i['properties']['SOATE']}-{random.randint(400, 800)}-{random.randint(1, 800)}"
    #                 contour = Contour.objects.create(ink=ink, conton_id=27, code_soato=code_soate)
    #                 ins = ContourYear.objects.create(polygon=geom, type_id=2, year='2022', productivity=uroj, code_soato=code_soate)
    #                 ins.contour.add(contour.pk)
    #             except Exception as e:
    #                 print(e)
    #     return Response('OK')


"""      
 Пашня 
     def get(self, request):
        with open('qwer.geojson') as f:
            data = json.load(f)['features']
            for i in data:
                try:
                    ink = f"{random.randint(400,500)}-02-123-{random.randint(2000,9000)}-78-{random.randint(1,350)}"
                    contour = Contour.objects.create(ink=ink, conton_id=10)
                    ins = ContourYear.objects.create(polygon=GEOSGeometry(f"{i['geometry']}"), type_id=1, year='2022')
                    ins.contour.add(contour.pk)
                    # ins.contour.set(2761)
                    # ins.save()
                except Exception as e:
                    print(e)
            return Response('OK')
"""

"""
 Пастбища
    def get(self, request):
        with open('pasture_cords.geojson') as f:
            data = json.load(f)['features']
            a = {'Садыр аке': 9, 'Тору-Айгырский': 11, 'Семеновский': 12, 'Орюктинский': 13, 'Кара-Ойский': 14,
                'Темировский': 15, 'Ананьевский': 16, 'Бостеринский': 17, 'Кум-Бельский': 18,
                'Тамчынский': 19, 'Абдрахмановский': 20, 'Чон-Сары-Ойский': 21}
            for i in data:
                code_soate = f"{i['properties']['SOATE']}-{random.randint(400,800)}-{random.randint(1,800)}"
                if i['properties']['Name_aa'] in a.keys():
                    contour = Contour.objects.create(code_soato=code_soate, conton_id=a.get(i['properties']['Name_aa']))
                    ins = ContourYear.objects.create(polygon=GEOSGeometry(f"{i['geometry']}"),
                                                     productivity=i['properties']['Urojainost'],
                                                     type_id=2, year='2022')
                    ins.contour.add(contour.pk)
            return Response('OK')
"""