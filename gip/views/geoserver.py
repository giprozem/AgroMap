# import requests
from geo.Geoserver import Geoserver
from osgeo import gdal

# from osgeo import gdal
# # # Initialize the library
# geo = Geoserver('https://geoserver.24mycrm.com/geoserver', username='admin', password='QjtUKPHMj46DHck')
# print(geo.create_coveragestore(workspace='Issyk-Kul', layer_name='demo_layer', path='../../tiff/-issyk- (15).tif'))
# # print(geo.get_layergroup(layer_name='-issyk-'))
# # print(geo.get_layergroups(workspace='Issyk-Kul'))
# # For creating workspace
# # geo.create_workspace(workspace='Issyk-Kul')
#
# # For uploading raster data to the geoserver
# geo.create_coveragestore(layer_name='group_layer_python_B08', path=r'../../tiff/output/mosaic_output_B08.tif', workspace='Issyk-Kul')
# # print(geo.publish_style(layer_name='layer_4', workspace='Issyk-Kul', style_name='raster'))
# # print(geo.get_layergroup(layer_name='North Yssyk-Kul crop', workspace='Issyk-Kul'))
#
#
# # url = 'https://geoserver.24mycrm.com/geoserver/rest/workspaces/my_workspace/datastores/my_datastore/featuretypes'
# # url = 'https://geoserver.24mycrm.com/geoserver/Issyk-Kul/wms?service=WMS&LAYERS=crop'
# # headers = {'Content-Type': 'text/xml'}
# # auth = ('admin', 'QjtUKPHMj46DHck')
# #
# # # define your XML string that you want to send to the server
# # data = """
# #     <featureType>
# #     <name>layer_1</name>
# #     <srs>EPSG:4326</srs>
# #     <enabled>true</enabled>
# #     <metadata>
# #     <entry key="time">
# #     <dimensionInfo>
# #     <enabled>true</enabled>
# #     <attribute>datetime</attribute>
# #     <presentation>CONTINUOUS_INTERVAL</presentation>
# #     <units>ISO8601</units>
# #     <defaultValue><strategy>MAXIMUM</strategy></defaultValue>
# #     </dimensionInfo>
# #     </entry>
# #     </metadata>
# #     <store class="dataStore">
# #         <name>my_datastore</name>
# #     </store>
# # </featureType>
# # """
# #
# # # fire the request
# # r = requests.post(url, headers=headers, auth=auth, data=data)
# #
# # # inspect the response
# # print(r.text)
#
# # inputpath = "https://geoserver.24mycrm.com/geoserver/Issyk-Kul/wcs?service=WCS&version=2.0.1&request=GetCoverage&CoverageId=layer_4&format=image/tiff"
# # inputpath = "https://geoserver.24mycrm.com/geoserver/gwc/service/wmts?&service=WMTS&request=GetTile&version=1.0.0&layer=I-K&style=raster&tilematrixset=EPSG:32643&format=image/png"
# # inputpath = "https://geoserver.24mycrm.com/geoserver/gwc/service/wmts?&service=WMTS&request=GetTile&version=1.0.0&layer=spearfish&style=&tilematrixset=EPSG:900913&format=image/png&tilematrix=EPSG:900913:16tilerow=24685&tilecol=46018"
# # inputpath = "https://geoserver.24mycrm.com/geoserver/gwc/service/wmts?&service=WMTS&request=GetTile&version=1.0.0&layer=-issyk-&style=raster&tilematrixset=EPSG:4326&format=image/png&tilematrix=EPSG:4326:21&tilerow=543478&tilecol=2970962"
#
# # "https://geoserver.24mycrm.com/geoserver/Issyk-Kul/wms?service=WMS&version=1.1.1&request=DescribeLayer&layers=-issyk-&format=image/tiff"
# #
# #
# # inputpath = "https://geoserver.24mycrm.com/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=-issyk-&format=application/openlayers&srs=EPSG:32643&bbox=499980,4690200,809760,4800000&width=768&height=330"
# # outputpath = '../../tiff/output/group_layers.tiff'
# outputpath = '../../tiff/output/layer_geoserver.tif'
# outputpath = '../../tiff/output/test.tif'
# polygon = r'../../tiff/map.geojson'
# # #
# inputpath = '../../tiff/output/mosaic_output.tif'
# # inputpath = 'https://geoserver.24mycrm.com/geoserver/Issyk-Kul/wcs?service=WCS&version=2.0.1&request=GetCoverage&CoverageId=north_tiff&format=image/tiff'
# def cutting_tiff():
#     gdal.Warp(destNameOrDestDS=outputpath,
#               srcDSOrSrcDSTab=inputpath,
#               cutlineDSName=polygon,
#               cropToCutline=True,
#               copyMetadata=True,
#               dstNodata=0)
#
#
# if __name__ == '__main__':
#     cutting_tiff()

#
#
#
#
# # from owslib.csw import CatalogueServiceWeb
# # import urllib
# #
# # def getLinkByIDCWS(url, id, user, pwd):
# #     csw = CatalogueServiceWeb(url, username=user, password=pwd)
# #
# #     csw.getrecordbyid(id=[id])
# #     csw.records[id].references
# #
# #     link = csw.records[id].references[2]['url']
# #
# #     return link
# #
# # def downloadImage(url, fileName):
# #     urllib.request.urlretrieve(url, fileName)
# #
# # # url = "https://geoserver.24mycrm.com/geoserver/csw?service=CSW&version=2.0.2&request=GetRecords&typeNames=gmd:MD_Metadata&resultType=results&elementSetName=full&outputSchema=http://www.isotc211.org/2005/gmd"
# # url = "https://geoserver.24mycrm.com/geoserver/wmts?"
# # record = "Issyk-Kul:layer_4"
# # name = "admin"
# # pwd = "QjtUKPHMj46DHck"
# #
# # link = getLinkByIDCWS(url, record, name, pwd)
# # print(link)
# #
# # downloadImage(link, "test.arc")
#
#
# # # a = "http://localhost:8080/geoserver/" + workspace[0] + "/wcs?service=WCS&version=2.0.1&request=GetCoverage&CoverageId=" + layer.params.LAYERS + "&format=image/tiff"
# # a = "https://geoserver.24mycrm.com/geoserver/Issyk-Kul/wcs?service=WCS&version=2.0.1&request=GetCoverage&CoverageId=layer_4&format=image/tiff"
# # headers = {
# #     'username': 'admin',
# #     'password': 'QjtUKPHMj46DHck'
# # }
# # print(requests.get(a).text)
#
# """
# https://geoserver.24mycrm.com/geoserver/<workspace>/wms?service=WMS&version=1.1.0&request=GetMap&layers=<workspace>:<layer_group_name>&format=image/tiff&srs=<srs>&bbox=<bbox>&width=<width>&height=<height>
# https://geoserver.24mycrm.com/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=-issyk-&format=image/geotiff&srs=EPSG:32643&bbox=499980,4690200,809760,4800000&WIDTH=3000&HEIGHT=1000
#
# """
#
# # import rasterio
# # from rasterio import plot
# #
# #
# # with rasterio.open('../../tiff/data/20220828_B08.tif') as f:
# #     print(f.meta)
# #     plot.show(f)
#
#
#
# # import requests
# # import json
# # #
# # url = "https://geoserver.24mycrm.com/geoserver/rest/layergroups/-issyk-.json"
# #
# # auth = ('admin', 'QjtUKPHMj46DHck')
# #
# # response = requests.get(url, auth=auth)
# # if response.status_code == 200:
# #     data = json.loads(response.content)
# #     # print(data["layerGroup"]["bounds"])
# #     # bbox = data["layerGroup"]["bounds"]["nativeBounds"]
# #     # print(bbox)
# #     bbox = data["layerGroup"]["bounds"]
# #     srs = bbox['crs']['$']
# #
# #     a = f"https://geoserver.24mycrm.com/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=-issyk-&format=image/geotiff&srs={srs}&bbox={bbox['minx']},{bbox['miny']},{bbox['maxx']},{bbox['maxy']}&WIDTH=3000&HEIGHT=1000"
# #     response = requests.get(a)
# #     with open('layer.tiff', "wb") as f:
# #         print(f.write(response.content))
#
#
# from django.contrib.gis.geos import GEOSGeometry
#
# # a = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"coordinates":[[[77.71434669540247,42.771522496633594],[77.71434669540247,42.694304425607584],[77.8217586218239,42.694304425607584],[77.8217586218239,42.771522496633594],[77.71434669540247,42.771522496633594]]],"type":"Polygon"}}]}
# # b = GEOSGeometry(f"{a['features'][0]['geometry']}")
# # print(b)
#
# # url = f"https://geoserver.24mycrm.com/geoserver/wfs?request=GetFeature&typeName=north_tiff_1&outputFormat=image/geotiff&CQL_FILTER=((77.71434669540247 42.771522496633594, 77.71434669540247 42.694304425607584, 77.8217586218239 42.694304425607584, 77.8217586218239 42.771522496633594, 77.71434669540247 42.771522496633594))"
#
# # response = requests.get(url)
#
# # if response.status_code == 200:
# #     with open("geotiff.tiff", "wb") as f:
# #         f.write(response.content)
# #         print(f)
#
#
# # width and height loyer_group
# """
# https://geoserver.24mycrm.com/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=-issyk-&format=image/geotiff&srs=EPSG:32643&bbox=499980,4690200,809760,4800000&width=6000&height=3000
# https://geoserver.24mycrm.com/geoserver/wms?service=WMS&version=1.3.0&request=GetMap&layers=issyk&format=image/geotiff
# https://geoserver.24mycrm.com/geoserver/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=-issyk-&outputFormat=image/tiff.
# https://geoserver.24mycrm.com/geoserver/Issyk-Kul/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=Issyk-Kul:north_tiff&outputFormat=image/geotiff
# https://geoserver.24mycrm.com/geoserver/workspaces/Issyk-Kul/ows?service=WFS&version=1.0.0&request=GetFeature&outputFormat=image/geotiff
# """

# from tifffile import imread, imwrite
# import numpy as np
#
# r = imread('../../tiff/group/20220805_B04.tif')
# g = imread('../../tiff/group/20220825_B04.tif')
# b = imread('../../tiff/group/20220828_B04.tif')
# RGB = np.dstack((r,g,b))
# imwrite('result.tif', RGB)

# from PIL import Image
#
# import os
#
# path_to_file = '../../tiff/group'
#
# images = []
#
# for i in os.listdir(path_to_file):
#     with Image.open(path_to_file + '/' + i) as im:
#         images.append(im.copy())
#
# print(Image.new(images[0].mode, (images[0].size[0] * 3, images[0].size[1] * 5)))

# new_image = Image.new(images[0].mode, (images[0].size[0] * 3, images[0].size[1] * 5))

# new_image.paste(images[0])
# new_image.paste(images[1], (images[0].size[0] * 1, 0))
# new_image.paste(images[2], (images[0].size[0] * 2, 0))
#
# new_image.show()



from rasterio.plot import show
from rasterio.merge import merge
from rasterio import plot
import rasterio as rio
from pathlib import Path
path = Path('../../tiff/group')
Path('output').mkdir(parents=True, exist_ok=True)
output_path = '../../tiff/output/mosaic_output_2_layer.tif'
raster_files = list(path.iterdir())
raster_to_mosiac = []
for p in raster_files:
    raster = rio.open(p)
    raster_to_mosiac.append(raster)

mosaic, output = merge(raster_to_mosiac)

output_meta = raster.meta.copy()
output_meta.update(
    {"driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": output,
    }
)

with rio.open(output_path, "w", **output_meta) as m:
    m.write(mosaic)


with rio.open(output_path) as f:
    plot.show(f)
