from django.contrib.gis.geos import GEOSGeometry
from osgeo import gdal
from rest_framework.serializers import ModelSerializer

from indexes.models import NDVIIndex
from gip.serializers.contour import ContourSerializer


class NDVISerializer(ModelSerializer):

    class Meta:
        model = NDVIIndex
        fields = '__all__'

    def remove_file(self, deleting_path):
        import os
        if os.path.isfile(deleting_path):
            os.remove(deleting_path)

    def ndvi_calculator(self, B04, B8A):
        import matplotlib.pyplot as plt
        import numpy
        from io import BytesIO
        import rasterio
        from django.core.files.base import ContentFile

        with rasterio.open(f'./media/{B04}') as src:
            band_red = src.read(1)

        with rasterio.open(f'./media/{B8A}') as f:
            band_nir = f.read(1)

        # Allow division by zero
        numpy.seterr(divide='ignore', invalid='ignore')

        # # Calculate NDVI
        ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)

        min_value = numpy.nanmin(ndvi)
        max_value = numpy.nanmax(ndvi)
        mid = 0.1

        fig = plt.figure(figsize=(75, 25))
        ax = fig.add_subplot(111)

        cmap = plt.cm.YlGn
        cax = ax.imshow(ndvi, cmap=cmap, clim=(min_value, max_value), vmin=min_value, vmax=max_value)

        ax.axis('off')

        f = BytesIO()

        plt.savefig(f, format='png', transparent=True, bbox_inches='tight')
        content_file = ContentFile(f.getvalue())
        return content_file

    def cutting_tiff(self, outputpath, inputpath, converted_polygon):
        gdal.Warp(destNameOrDestDS=f'{outputpath}',
                  srcDSOrSrcDSTab=inputpath,
                  cutlineDSName=f'{converted_polygon}',
                  cropToCutline=True,
                  copyMetadata=True,
                  dstNodata=0)

    def create(self, validated_data):
        converted_polygon = GEOSGeometry(validated_data['contour'].polygon).geojson

        writing_file = f'{validated_data["contour"].ink}'
        obj = NDVIIndex.objects.create(
            contour=validated_data['contour'],
            date_of_satellite_image=validated_data['date_of_satellite_image']
        )
        B8A = f'B8A{writing_file}.tiff'
        B04 = f'B04{writing_file}.tiff'
        # TODO after uploading satellite images refactor
        if validated_data['date_of_satellite_image'] == 'Весна':
            inputpath_B8A = './satellite_images/B8A_spring.tiff'
        elif validated_data['date_of_satellite_image'] == 'Лето':
            inputpath_B8A = "./satellite_images/B8A.tiff"
        else:
            inputpath_B8A = "./satellite_images/B8A_autum.tiff"

        outputpath_B8A = f"./media/{B8A}"

        self.cutting_tiff(outputpath=outputpath_B8A, inputpath=inputpath_B8A, converted_polygon=converted_polygon)
        # TODO after uploading satellite images refactor
        if validated_data['date_of_satellite_image'] == 'Весна':
            inputpath_B04 = './satellite_images/B04_spring.tiff'
        elif validated_data['date_of_satellite_image'] == 'Лето':
            inputpath_B04 = "./satellite_images/B04.tiff"
        else:
            inputpath_B04 = "./satellite_images/B04_autum.tiff"

        outputpath_B04 = f"./media/{B04}"
        self.cutting_tiff(outputpath=outputpath_B04, inputpath=inputpath_B04, converted_polygon=converted_polygon)

        obj.ndvi_image.save(f'ndvi{writing_file}.png', self.ndvi_calculator(B04=B04, B8A=B8A))

        self.remove_file(outputpath_B04)
        self.remove_file(outputpath_B8A)

        return obj


class NDVIListSerializer(ModelSerializer):
    contour = ContourSerializer()

    class Meta:
        model = NDVIIndex
        fields = '__all__'
