from django.contrib.gis.geos import GEOSGeometry
from faker import Faker


def get_polygon():
    long = Faker().pyfloat(right_digits=6, positive=True, min_value=70, max_value=80)
    lat = Faker().pyfloat(right_digits=6, positive=True, min_value=39, max_value=43)
    polygon = [
        [long, lat],
        [
            Faker().pyfloat(right_digits=6, positive=True, min_value=70, max_value=80),
            Faker().pyfloat(right_digits=6, positive=True, min_value=39, max_value=43),
        ],
        [
            Faker().pyfloat(right_digits=6, positive=True, min_value=70, max_value=80),
            Faker().pyfloat(right_digits=6, positive=True, min_value=39, max_value=43),
        ],
        [
            Faker().pyfloat(right_digits=6, positive=True, min_value=70, max_value=80),
            Faker().pyfloat(right_digits=6, positive=True, min_value=39, max_value=43),
        ],
        [long, lat],
    ]
    geojson = {"type": "Polygon", "coordinates": [polygon]}
    return GEOSGeometry(f"{geojson}")
