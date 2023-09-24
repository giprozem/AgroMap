import datetime
from rest_framework import serializers
from django.db import connection
from ai.models.predicted_contour import Contour_AI
from gip.models import Conton
from gip.serializers.culture import CultureSerializer
from gip.serializers.landtype import LandTypeSerializer
from gip.serializers.soil import SoilClassSerializer
from gip.views.handbook_contour import contour_Kyrgyzstan
from rest_framework.exceptions import APIException


# Serializer for Contour_AI model
class Contour_AISerializer(serializers.ModelSerializer):
    # Nested serializers for related fields
    soil_class = SoilClassSerializer()
    type = LandTypeSerializer()
    culture = CultureSerializer()

    class Meta:
        model = Contour_AI
        fields = '__all__'  # Serialize all fields from the Contour_AI model

    # Custom representation method to add nested region and district data
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Add region information if district exists
        representation['region'] = {
            'id': instance.district.region.pk if instance.district else None,
            'name_ru': instance.district.region.name_ru if instance.district else None,
            'name_ky': instance.district.region.name_ky if instance.district else None,
            'name_en': instance.district.region.name_en if instance.district else None,
            'code_soato': instance.district.region.code_soato if instance.district else None,
        }

        # Add district information if district exists
        representation['district'] = {
            'id': instance.district.pk if instance.district else None,
            'name_ru': instance.district.name_ru if instance.district else None,
            'name_ky': instance.district.name_ky if instance.district else None,
            'name_en': instance.district.name_en if instance.district else None,
            'code_soato': instance.district.code_soato if instance.district else None,
        }

        return representation


# Serializer for updating Contour_AI model
class UpdateContour_AISerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour_AI
        fields = '__all__'  # Serialize all fields from the Contour_AI model

    # Custom representation method to add region_id and district_id fields
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['region_id'] = instance.conton.district.region.pk if instance.conton.district.region else None
        representation['district_id'] = instance.conton.district.pk if instance.conton.district else None
        return representation

    # Method to check if a polygon is inside Kyrgyzstan
    def is_polygon_inside_Kyrgyzstan(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT ST_Contains('{contour_Kyrgyzstan}'::geography::geometry, '{request}'::geography::geometry);
            """)
            inside = cursor.fetchall()
        return inside[0][0]

    # Method to get the district ID based on the polygon
    def get_district(self, attrs):
        with connection.cursor() as cursor:
            cursor.execute(f"""
            SELECT dst.id FROM gip_district AS dst WHERE ST_Contains(dst.polygon::geography::geometry,
            '{attrs['polygon']}'::geography::geometry);
            """)
            district = cursor.fetchall()
        return district[0][0]

    # Method to get the district ID from the database
    def get_db_district(self, attrs):
        db_district = [i.district.pk if i.district else None for i in Conton.objects.filter(id=attrs['conton'].pk)]
        return db_district[0]

    # Method to validate the district
    def validate_district(self, attrs):
        district = self.get_district(attrs)
        db_district = self.get_db_district(attrs)
        if district != db_district:
            raise APIException({
                "message": f"Your contour goes beyond the boundaries of <{attrs['conton']}>"
            })

    # Method to validate the year
    def is_valid_year(self, attrs):
        if int(attrs['year']) > datetime.date.today().year:
            raise APIException({"message": "Year cannot be greater than the current year"})
        elif int(attrs['year']) < 2010:
            raise APIException({"message": "Year should be at least 2010"})

    # Custom validation method for the serializer
    def validate(self, attrs):
        if not self.is_polygon_inside_Kyrgyzstan(attrs['polygon']):
            raise APIException({"message": "Create a field within Kyrgyzstan"})

        self.validate_district(attrs)

        self.is_valid_year(attrs)

        return attrs