from ai.models.predicted_contour import Contour_AI
import rasterio
from rasterio import warp


def main():
    data = []
    coordinates = Contour_AI.objects.all()
    for i in coordinates:
        data.append(i.polygon.wkt)

    with rasterio.open('media/cutted_tiff/tile_0_20546084632.tif') as src:
        bbox_m = src.bounds
        bbox = warp.transform_bounds(src.crs, {'init': 'EPSG:4326'}, *bbox_m)

    print(bbox[2]-bbox[0],bbox[3]-bbox[1])
    print(data[0])
    # with open("data.txt", "w") as txt_file:
    #     for line in data:
    #         txt_file.write(line + "\n")
