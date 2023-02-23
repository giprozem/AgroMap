import datetime
from threading import Thread

from django.contrib.gis.geos import GEOSGeometry
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import ContourYear
from indexes.models import SciHubImageDate
from indexes.index_funcs.common_funcs import cutting_tiff
from indexes.utils import veg_index_creating


class TestAPIView(APIView):
    def get(self, request):
        print('get')
        # image_dates = SciHubImageDate.objects.all()
        # file_name = f'временный файл {datetime.datetime.now()}'
        # for image_date in image_dates:
        #     contours = ContourYear.objects.filter(polygon__coveredby=image_date.polygon)
        #     print(f'image data === {image_date}')
        #     print('inside')
            # input_path_b01 = f"./media/{image_date.B01}"
            # input_path_b02 = f"./media/{image_date.B02}"
            # input_path_b03 = f"./media/{image_date.B03}"
            # input_path_b04 = f"./media/{image_date.B04}"
            # input_path_b05 = f"./media/{image_date.B05}"
            # input_path_b06 = f"./media/{image_date.B06}"
            # input_path_b07 = f"./media/{image_date.B07}"
            # input_path_b8a = f"./media/{image_date.B8A}"
            # input_path_b09 = f"./media/{image_date.B09}"
            # input_path_b11 = f"./media/{image_date.B11}"
            # input_path_b12 = f"./media/{image_date.B12}"
            #
            # output_path_b01 = f"./media/cut/B01_{file_name}.tiff"
            # output_path_b02 = f"./media/cut/B02_{file_name}.tiff"
            # output_path_b03 = f"./media/cut/B03_{file_name}.tiff"
            # output_path_b04 = f"./media/cut/B04_{file_name}.tiff"
            # output_path_b05 = f"./media/cut/B05_{file_name}.tiff"
            # output_path_b06 = f"./media/cut/B06_{file_name}.tiff"
            # output_path_b07 = f"./media/cut/B07_{file_name}.tiff"
            # output_path_b8a = f"./media/cut/B08a_{file_name}.tiff"
            # output_path_b09 = f"./media/cut/B09_{file_name}.tiff"
            # output_path_b11 = f"./media/cut/B11_{file_name}.tiff"
            # output_path_b12 = f"./media/cut/B12_{file_name}.tiff"
            # for contour in contours:
            #     polygon = GEOSGeometry(contour.polygon).geojson
            #     print(contour.id)
                # cutting_tiff(outputpath=output_path_b01, inputpath=input_path_b01, polygon=polygon)
                # cutting_tiff(outputpath=output_path_b02, inputpath=input_path_b02, polygon=contour)
                # cutting_tiff(outputpath=output_path_b03, inputpath=input_path_b03, polygon=contour)
                # cutting_tiff(outputpath=output_path_b04, inputpath=input_path_b04, polygon=contour)
                # cutting_tiff(outputpath=output_path_b05, inputpath=input_path_b05, polygon=contour)
                # cutting_tiff(outputpath=output_path_b06, inputpath=input_path_b06, polygon=contour)
                # cutting_tiff(outputpath=output_path_b07, inputpath=input_path_b07, polygon=contour)
                # cutting_tiff(outputpath=output_path_b8a, inputpath=input_path_b8a, polygon=contour)
                # cutting_tiff(outputpath=output_path_b09, inputpath=input_path_b09, polygon=contour)
                # cutting_tiff(outputpath=output_path_b11, inputpath=input_path_b11, polygon=contour)
                # cutting_tiff(outputpath=output_path_b12, inputpath=input_path_b12, polygon=contour)
        thread_object = Thread(target=veg_index_creating)
        thread_object.start()
        return Response('Ok')
