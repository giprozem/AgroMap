from ai.models.predicted_contour import Contour_AI
import rasterio
from rasterio import warp
import numpy as np
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Intersection

def main():
    data = []
    coordinates = Contour_AI.objects.filter(image_id=4)
    for i in coordinates:
        data.append(i.polygon.wkt)

    with rasterio.open('media/cutted_tiff/tile_0_20546084632.tif') as src:
        bbox_m = src.bounds
        bbox = warp.transform_bounds(src.crs, {'init': 'EPSG:4326'}, *bbox_m)

    x = bbox[2]-bbox[0]
    y = bbox[3]-bbox[1]

    myarray = []
    for line in data:
        line = line.replace('POLYGON ', '').removesuffix('))').removeprefix('((')
        line = line.split(', ')
        array = []
        for j in line:
            j = j.split(' ')
            long = float(j[0]) - bbox[0]
            lat = float(j[1]) - bbox[1]
            array.append([long / x, 1 - lat / y])

        myarray.append(np.float32(array))
    with open("data.txt", "w") as txt_file:
       for s in myarray:
           for i in s:
            txt_file.write(f'{i[0]} {i[1]}')


def clean():
    contours = Contour_AI.objects.all()
    intersections = []
    for i in contours:
        #for c in Contour_AI.objects.exclude(id=i.pk).filter(polygon__intersects=i.polygon.wkt):
            #intersections.append([i.intersection(c.polygon.wkt), i.pk])
        results = Intersection(Contour_AI.objects.exclude(id=i.pk), i.polygon.wkt)
    print(results)