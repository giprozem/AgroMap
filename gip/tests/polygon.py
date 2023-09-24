# Import necessary modules
from django.contrib.gis.geos import GEOSGeometry

# Define a function for creating a GEOSGeometry representing a polygon
def get_polygon():

    """
    Generate mock polygon without Faker, using static data
    """

    # Define a dictionary representing a polygon's coordinates
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

    # Create a GeoJSON representation of the polygon
    geojson = {
        "type": "Polygon",
        "coordinates": polygon_dict["geometry"].get("coordinates"),
    }

    # Create a GEOSGeometry object from the GeoJSON representation
    return GEOSGeometry(f"{geojson}")
