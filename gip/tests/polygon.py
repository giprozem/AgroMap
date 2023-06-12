from django.contrib.gis.geos import GEOSGeometry
from faker import Faker


def get_polygon():
    long = Faker().pyfloat(right_digits=6, positive=True, min_value=71, max_value=79)
    lat = Faker().pyfloat(right_digits=6, positive=True, min_value=40, max_value=42)
    polygon = [[long, lat],
               [Faker().pyfloat(right_digits=6, positive=True, min_value=71, max_value=79),
                Faker().pyfloat(right_digits=6, positive=True, min_value=40, max_value=42)],
               [Faker().pyfloat(right_digits=6, positive=True, min_value=71, max_value=79),
                Faker().pyfloat(right_digits=6, positive=True, min_value=40, max_value=42)],
               [Faker().pyfloat(right_digits=6, positive=True, min_value=71, max_value=79),
                Faker().pyfloat(right_digits=6, positive=True, min_value=40, max_value=42)],
               [long, lat]]
    geojson = {
        "type": "Polygon",
        "coordinates": [polygon]
    }
    return GEOSGeometry(f"{geojson}")
