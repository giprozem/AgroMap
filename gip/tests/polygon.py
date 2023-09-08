from django.contrib.gis.geos import GEOSGeometry
from faker import Faker


def get_polygon():
    fake = Faker()
    long = fake.pyfloat(right_digits=6, positive=True, min_value=69, max_value=81 - 1e-6)  # Максимум вычитаем небольшое значение, чтобы исключить 81
    lat = fake.pyfloat(right_digits=6, positive=True, min_value=38, max_value=44)
    polygon = [
        [long, lat],
        [
            fake.pyfloat(right_digits=6, positive=True, min_value=69, max_value=81 - 1e-6),
            fake.pyfloat(right_digits=6, positive=True, min_value=38, max_value=44),
        ],
        [
            fake.pyfloat(right_digits=6, positive=True, min_value=69, max_value=81 - 1e-6),
            fake.pyfloat(right_digits=6, positive=True, min_value=38, max_value=44),
        ],
        [
            fake.pyfloat(right_digits=6, positive=True, min_value=69, max_value=81 - 1e-6),
            fake.pyfloat(right_digits=6, positive=True, min_value=38, max_value=44),
        ],
        [long, lat],
    ]
    geojson = {"type": "Polygon", "coordinates": [polygon]}
    return GEOSGeometry(f"{geojson}")
