from rest_framework.response import Response
from rest_framework.views import APIView
from ai.utils.predicted_contour import create_rgb, cut_rgb_tif, merge_bands, deleted_files, yolo
import os
from ai.models import Contour_AI, Images_AI, Yolo
from ultralytics import YOLO
import rasterio
from PIL import Image
from pyproj import Proj, transform
from django.contrib.gis.geos import Polygon
import matplotlib.pyplot as plt
import pandas as pd


class CutAPIView(APIView):
    def get(self, request):
        merge_bands()
        create_rgb()
        cut_rgb_tif()
        deleted_files()
        yolo()
        return Response({"message": "ok"})

