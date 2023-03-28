from rest_framework.response import Response
from rest_framework.views import APIView
from ai.utils import create_rgb, cut_image
import shutil
import os
from ai.models import Contour, Images, Yolo
from ultralytics import YOLO
import rasterio
from PIL import Image
from pyproj import Proj, transform
from django.contrib.gis.geos import Polygon


class CutAPIView(APIView):
    def post(self, request):
        create_rgb()
        cut_image()
        return Response({"message": "ok"})


class PredictAPIView(APIView):
    def get(self, request, *args, **kwargs):
        file = Yolo.objects.get(id=1)
        model = YOLO(f'media/{file.ai}')
        image = Image.open('media/rgb/file.tif')
        results = model.predict(source=image, save=True, conf=0.9)
        arrays = results[0].masks.segments
        confs = results[0].boxes.conf
        images = Images.objects.create()
        images.image.save(os.listdir('runs/segment/predict/')[0],
                          open(f"runs/segment/predict/{os.listdir('runs/segment/predict/')[0]}", 'rb'))
        w, h = image.size
        x = 1 / w
        y = 1 / h
        with rasterio.open('media/rgb/file.tif') as src:
            for n in range(0, len(arrays)):
                coordinates = []
                for i in arrays[n]:
                    coordinates.append(src.xy(i[1]/x, i[0]/y))
                coordinates.append(coordinates[0])
                geojson = []
                for i in range(0, len(coordinates)):
                    inProj = Proj(init=f'epsg:{src.crs.to_epsg()}')
                    outProj = Proj(init='epsg:4326')
                    x1, y1 = coordinates[i][0], coordinates[i][1]
                    x2, y2 = transform(inProj, outProj, x1, y1)
                    geojson.append([x2, y2])
                geojson = tuple(geojson)
                conf = confs[n]
                poly = Polygon(geojson)
                Contour.objects.create(polygon=poly, percent=conf)
            shutil.rmtree('runs')
        return Response({"message": "ok"})
