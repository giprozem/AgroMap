import json
import random

from django.contrib.gis.geos import GEOSGeometry
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import District, Contour, ContourYear


# print(GEOSGeometry('{"type": "Polygon", "coordinates": [[[  78.44393926260682,  42.68050688095687],[  78.4462975804604,  42.68813482667355],[  78.44110478403718,  42.69336529789743],[  78.4314884943629,  42.69336529789743],[  78.42764197847265,  42.67456832793974],[  78.44316995943262,  42.67060897482594],[  78.4627871903653,  42.67089179402163],[  78.46874928996272,  42.675982319480426],[  78.4635564935395,  42.6820621228741],[  78.45874834870233,  42.67951716128536],[  78.45932532608242,  42.68587936980282],[  78.44393926260682,  42.68050688095687]]]}}'))



class GeojsonSavingToDBAPIView(APIView):
    pass


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