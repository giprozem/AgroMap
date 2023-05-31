import datetime
import json
import random
import time

from django.contrib.gis.geos import GEOSGeometry
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import District, Contour, Conton
from django.contrib.gis.geos.prototypes.io import wkt_w
import datetime

from gip.serializers.contour import CalculatePolygonContourSerializer


class GeojsonSavingToDBAPIView(APIView):

    def post(self, request, *args, **kwargs):
        start = datetime.datetime.now()

        def average(lst):
            return sum(lst) / len(lst)

        with open('t-t.geojson') as f:
            data = json.load(f)['features']
            f.readlines()
            print('raion')
            raion = 0
            for i in data:
                raion += 1
                try:
                    uroj = i['properties']['Urojainost']
                    uroj = uroj.replace(',', '.')
                    uroj = uroj.replace('-', ',')
                    lst = [float(x) for x in uroj.split(',')]
                    b = []
                    for j in lst:
                        b.append(float(j))
                    result = average(b)
                    print(f'average=== {result}')
                    a = {'Ак-Терекский': 66, 'Болот Мамбетовский': 69, 'Каджи-Сайский': 65, 'Кок-Мойнокский': 68, 'Колторский а.а': 67,
                         'Кун-Чыгышский': 70, 'Торт-Кульский': 72, 'Тонский': 71, 'Улахолский': 73,
                         "Тогуз-Булакский": 77,
                         "Сары-Булакский": 79,
                         "Ак-Булунский": 80,
                         "Аралский": 24,
                         "Иссык-Кельский": 74,
                         "Карасаевский": 81,
                         "Кутургинский": 75,
                         "Михайловский": 76,
                         "Сан-Ташский-присельный-1": 78,
                         "Сан-Ташский-присельный-2": 78,
                         "Талды-Суйский": 3,
                         "Тюпский": 10,
                         "Чон-Ташский": 82
                         }
                    polygon = GEOSGeometry(f"{i['geometry']}")
                    wkt = wkt_w(dim=2).write(polygon).decode()
                    geom = GEOSGeometry(wkt, srid=4326)

                    contour = Contour.objects.create(
                        conton_id=a.get(i['properties']['Aiyl_aimak']),
                        polygon=geom,
                        year='2022',
                        productivity=result,
                        type_id=2
                    )
                    contour.save()
                    time.sleep(2)

                except Exception as e:
                    print(f'error === {e}')
                    print(i['properties']['Aiyl_aimak'])
                    with open('t-t-errors.txt', 'a') as file:
                        file.write(str(e))
                        file.write(str(raion))
                        file.write(',')
                        file.write('\n')
        print(start - datetime.datetime.now())

        return Response(raion, status=200)


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


class ContonWithoutPolygonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conton
        fields = ('id', 'name_ru',)


class ContonID(APIView):

    def get(self, request):
        conton = Conton.objects.filter(district_id=3).order_by('name_ru')
        serializer = ContonWithoutPolygonSerializer(conton, many=True).data
        result = {i['name_ru']: i['id'] for i in serializer}
        return Response(result, status=200)



"""

                    GEOS_ERROR: IllegalArgumentException: Invalid
                    number
                    of
                    points in LinearRing
                    found
                    3 - must
                    be
                    0 or >= 4

                    error == = Error
                    encountered
                    checking
                    Geometry
                    returned
                    from GEOS C
                    function
                    "GEOSWKBReader_read_r".
                    Сан - Ташский - присельный - 2
                    89
"""


class Dumping(APIView):

    def get(self, request):
        with open('null_index.txt', 'r') as f:
            data = f.readlines()
        contour = []
        for i in data:
            # contour_1 = Contour.objects.filter(id=int(i))
            contour_1 = Contour.objects.filter(id__range=(354, 359))
            serializer = CalculatePolygonContourSerializer(contour_1, many=True).data
            with open('contours.json', 'a') as file:
                file.write(str(serializer))
            # print(contour_1)
            # print(type(contour_1))
            # time.sleep(5)
            # contour.append(contour_1[0])
        # serializer = CalculatePolygonContourSerializer(contour, many=True).data
        return Response(contour, status=200)
