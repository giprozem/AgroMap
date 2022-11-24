# from shapely.geometry import Point, Polygon, MultiPolygon
from django.contrib.gis.geos import Polygon, Point

p1 = Point(74.61313199999999, 42.832171)

cords = [(74.58206199999999, 42.789858), (74.583778, 42.857595), (74.66308600000001, 42.855833), (74.66136899999999, 42.84501), (74.64901, 42.835696), (74.639397, 42.832926), (74.645233, 42.812781), (74.642143, 42.810262), (74.64557600000001, 42.802706), (74.609184, 42.804469), (74.592018, 42.801698), (74.58206199999999, 42.789858)]
a = "SRID=4326;MULTIPOLYGON (((75.28656005859374 42.82562425459299, 75.17120361328124 42.88200212690439, 75.10803222656249 42.85180609584703, 75.13000488281247 42.79943131987834, 75.26184082031249 42.78935416050277, 75.28656005859374 42.82562425459299)))"

" <class 'django.contrib.gis.geos.collections.MultiPolygon'>"
"<class 'shapely.geometry.polygon.Polygon'>"

poly = Polygon(cords)
# poly = MultiPolygon(cords)
# print(type(a))
# print(p1)
# print(type(poly))
# print(poly)

print(p1.within(poly))

"""
{
        "created_at": "2022-11-23T16:49:33.242413+06:00",
        "updated_at": "2022-11-23T16:49:33.242433+06:00",
        "polygon": "SRID=4326;POINT (74.61313199999999 42.832171)",
        "created_by": 1,
        "updated_by": 1,
        "conton": 1,
        "farmer": 1
    }
"""

"""
{
        "polygon": "SRID=4326;POINT (74.61313199999999 42.832171)"
    }
"""