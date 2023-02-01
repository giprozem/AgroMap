import requests
from geo.Geoserver import Geoserver
from osgeo import gdal
# Initialize the library
# geo = Geoserver('https://geoserver.24mycrm.com/geoserver', username='admin', password='QjtUKPHMj46DHck')

# For creating workspace
# geo.create_workspace(workspace='Issyk-Kul')

# For uploading raster data to the geoserver
# geo.create_coveragestore(layer_name='north_tiff_6', path=r'../../tiff/data/20220828_B08.tif', workspace='Issyk-Kul')
# print(geo.publish_style(layer_name='layer_4', workspace='Issyk-Kul', style_name='raster'))
# print(geo.get_layergroup(layer_name='North Yssyk-Kul crop', workspace='Issyk-Kul'))


# url = 'https://geoserver.24mycrm.com/geoserver/rest/workspaces/my_workspace/datastores/my_datastore/featuretypes'
# url = 'https://geoserver.24mycrm.com/geoserver/Issyk-Kul/wms?service=WMS&LAYERS=crop'
# headers = {'Content-Type': 'text/xml'}
# auth = ('admin', 'QjtUKPHMj46DHck')
#
# # define your XML string that you want to send to the server
# data = """
#     <featureType>
#     <name>layer_1</name>
#     <srs>EPSG:4326</srs>
#     <enabled>true</enabled>
#     <metadata>
#     <entry key="time">
#     <dimensionInfo>
#     <enabled>true</enabled>
#     <attribute>datetime</attribute>
#     <presentation>CONTINUOUS_INTERVAL</presentation>
#     <units>ISO8601</units>
#     <defaultValue><strategy>MAXIMUM</strategy></defaultValue>
#     </dimensionInfo>
#     </entry>
#     </metadata>
#     <store class="dataStore">
#         <name>my_datastore</name>
#     </store>
# </featureType>
# """
#
# # fire the request
# r = requests.post(url, headers=headers, auth=auth, data=data)
#
# # inspect the response
# print(r.text)

# inputpath = "https://geoserver.24mycrm.com/geoserver/Issyk-Kul/wcs?service=WCS&version=2.0.1&request=GetCoverage&CoverageId=layer_4&format=image/tiff"
# inputpath = "https://geoserver.24mycrm.com/geoserver/gwc/service/wmts?&service=WMTS&request=GetTile&version=1.0.0&layer=I-K&style=raster&tilematrixset=EPSG:32643&format=image/png"
# inputpath = "https://geoserver.24mycrm.com/geoserver/gwc/service/wmts?&service=WMTS&request=GetTile&version=1.0.0&layer=spearfish&style=&tilematrixset=EPSG:900913&format=image/png&tilematrix=EPSG:900913:16tilerow=24685&tilecol=46018"
# inputpath = "https://geoserver.24mycrm.com/geoserver/gwc/service/wmts?&service=WMTS&request=GetTile&version=1.0.0&layer=-issyk-&style=raster&tilematrixset=EPSG:4326&format=image/png&tilematrix=EPSG:4326:21&tilerow=543478&tilecol=2970962"

# "https://geoserver.24mycrm.com/geoserver/Issyk-Kul/wms?service=WMS&version=1.1.1&request=DescribeLayer&layers=-issyk-&format=image/tiff"
#
#
# inputpath = "https://geoserver.24mycrm.com/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=-issyk-&format=image/geotiff&srs=EPSG:32643&bbox=499980,4690200,809760,4800000&WIDTH=3000&HEIGHT=1098"
# outputpath = '../../tiff/test11.tiff'
# polygon = r'../../tiff/map.geojson'
#
#
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





# from owslib.csw import CatalogueServiceWeb
# import urllib
#
# def getLinkByIDCWS(url, id, user, pwd):
#     csw = CatalogueServiceWeb(url, username=user, password=pwd)
#
#     csw.getrecordbyid(id=[id])
#     csw.records[id].references
#
#     link = csw.records[id].references[2]['url']
#
#     return link
#
# def downloadImage(url, fileName):
#     urllib.request.urlretrieve(url, fileName)
#
# # url = "https://geoserver.24mycrm.com/geoserver/csw?service=CSW&version=2.0.2&request=GetRecords&typeNames=gmd:MD_Metadata&resultType=results&elementSetName=full&outputSchema=http://www.isotc211.org/2005/gmd"
# url = "https://geoserver.24mycrm.com/geoserver/wmts?"
# record = "Issyk-Kul:layer_4"
# name = "admin"
# pwd = "QjtUKPHMj46DHck"
#
# link = getLinkByIDCWS(url, record, name, pwd)
# print(link)
#
# downloadImage(link, "test.arc")


# # a = "http://localhost:8080/geoserver/" + workspace[0] + "/wcs?service=WCS&version=2.0.1&request=GetCoverage&CoverageId=" + layer.params.LAYERS + "&format=image/tiff"
# a = "https://geoserver.24mycrm.com/geoserver/Issyk-Kul/wcs?service=WCS&version=2.0.1&request=GetCoverage&CoverageId=layer_4&format=image/tiff"
# headers = {
#     'username': 'admin',
#     'password': 'QjtUKPHMj46DHck'
# }
# print(requests.get(a).text)

"""
https://geoserver.24mycrm.com/geoserver/<workspace>/wms?service=WMS&version=1.1.0&request=GetMap&layers=<workspace>:<layer_group_name>&format=image/tiff&srs=<srs>&bbox=<bbox>&width=<width>&height=<height>
https://geoserver.24mycrm.com/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=-issyk-&format=image/geotiff&srs=EPSG:32643&bbox=499980,4690200,809760,4800000&WIDTH=3000&HEIGHT=1000

"""

# import rasterio
# from rasterio import plot
#
#
# with rasterio.open('../../tiff/data/20220828_B08.tif') as f:
#     print(f.meta)
#     plot.show(f)



import requests
import json
#
url = "https://geoserver.24mycrm.com/geoserver/rest/layergroups/-issyk-.json"

auth = ('admin', 'QjtUKPHMj46DHck')

response = requests.get(url, auth=auth)
if response.status_code == 200:
    data = json.loads(response.content)
    # print(data["layerGroup"]["bounds"])
    # bbox = data["layerGroup"]["bounds"]["nativeBounds"]
    # print(bbox)
    bbox = data["layerGroup"]["bounds"]
    srs = bbox['crs']['$']

    a = f"https://geoserver.24mycrm.com/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=-issyk-&format=image/geotiff&srs={srs}&bbox={bbox['minx']},{bbox['miny']},{bbox['maxx']},{bbox['maxy']}&WIDTH=3000&HEIGHT=1000"
    response = requests.get(a)
    with open('layer.tiff', "wb") as f:
        print(f.write(response.content))


from django.contrib.gis.geos import GEOSGeometry

# a = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"coordinates":[[[77.71434669540247,42.771522496633594],[77.71434669540247,42.694304425607584],[77.8217586218239,42.694304425607584],[77.8217586218239,42.771522496633594],[77.71434669540247,42.771522496633594]]],"type":"Polygon"}}]}
# b = GEOSGeometry(f"{a['features'][0]['geometry']}")
# print(b)

# url = f"https://geoserver.24mycrm.com/geoserver/wfs?request=GetFeature&typeName=north_tiff_1&outputFormat=image/geotiff&CQL_FILTER=((77.71434669540247 42.771522496633594, 77.71434669540247 42.694304425607584, 77.8217586218239 42.694304425607584, 77.8217586218239 42.771522496633594, 77.71434669540247 42.771522496633594))"

# response = requests.get(url)

# if response.status_code == 200:
#     with open("geotiff.tiff", "wb") as f:
#         f.write(response.content)
#         print(f)