from django.contrib.gis.geos import GEOSGeometry
from faker import Faker


def get_polygon():
    polygon_dict = {
        "geometry": {
            "coordinates": [
                [
                    [74.46521231318079, 42.996632395068104],
                    [74.46521231318079, 42.681573303060475],
                    [74.7913890639827, 42.681573303060475],
                    [74.7913890639827, 42.996632395068104],
                    [74.46521231318079, 42.996632395068104],
                ]
            ],
            "type": "Polygon",
        },
    }
    geojson = {
        "type": "Polygon",
        "coordinates": polygon_dict["geometry"].get("coordinates"),
    }
    return GEOSGeometry(f"{geojson}")
