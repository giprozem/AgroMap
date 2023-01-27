import json
import random

from django.contrib.gis.geos import GEOSGeometry
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import District, Contour


# print(GEOSGeometry('{"type": "Polygon", "coordinates": [[[  78.44393926260682,  42.68050688095687],[  78.4462975804604,  42.68813482667355],[  78.44110478403718,  42.69336529789743],[  78.4314884943629,  42.69336529789743],[  78.42764197847265,  42.67456832793974],[  78.44316995943262,  42.67060897482594],[  78.4627871903653,  42.67089179402163],[  78.46874928996272,  42.675982319480426],[  78.4635564935395,  42.6820621228741],[  78.45874834870233,  42.67951716128536],[  78.45932532608242,  42.68587936980282],[  78.44393926260682,  42.68050688095687]]]}}'))



class GeojsonSavingToDBAPIView(APIView):

    def get(self, request):
        # with open('result.geojson') as f:
        with open('pasture_cords.geojson') as f:
            #json
            # data = json.load(f)
            # for i in data['features']:
            #     # district = i['id']
            #     coordinates = GEOSGeometry(f"{i['geometry']}")
            #     # print(district)
            #     print(coordinates)
                # District.objects.create(name=district, polygon=coordinates, region_id=1)

            #geojson
            # data = f.readlines()
            # print(eval(data[50]))
            data = json.load(f)['features']
            for i in data:
                try:
                    ink = f"417-02-123-4543-78-{random.randint(1200,9999)}"
                    # polygon = "{" + f""""type": "Polygon", "coordinates": {eval(i)['coordinates']}""" + "}"
                    # # print(polygon)
                    # # a = GEOSGeometry(polygon)
                    # Contour.objects.create(ink=ink, polygon=GEOSGeometry(polygon), type=1, farmer=1)
                    # print(GEOSGeometry(f"{i}"))
                    # print(i['geometry'])
                    # print(GEOSGeometry(f"{i['geometry']}"))
                    Contour.objects.create(ink=ink, polygon=GEOSGeometry(f"{i['geometry']}"), type_id=2, farmer_id=1, conton_id=9)
                except Exception as e:
                    print(e)
                # ink = f"417-02-123-4543-78-{random.randint(1200,9999)}"
                # polygon = "{" + f""""type": "Polygon", "coordinates": {i[97:-3]}""" + "}"
                # print(polygon)
                # Contour.objects.create(ink=ink, polygon=GEOSGeometry(f""))
            return Response('OK')



# with open('../../result.geojson') as f:
#     print(f.readlines())