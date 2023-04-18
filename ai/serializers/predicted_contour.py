import datetime
from rest_framework import serializers
from django.db import connection
from ai.models.predicted_contour import Contour_AI
from gip.models import Conton, Region
from gip.serializers.culture import CultureSerializer
from gip.serializers.landtype import LandTypeSerializer
from gip.serializers.soil import SoilClassSerializer
from gip.views.handbook_contour import contour_Kyrgyzstan
from rest_framework.exceptions import APIException


class Contour_AISerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField()
    soil_class = SoilClassSerializer()
    type = LandTypeSerializer()
    culture = CultureSerializer()

    def get_region(self, obj):
        region = Region.objects.get(name=obj.district.region)
        return region.pk

    class Meta:
        model = Contour_AI
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['region'] = {
            'id': instance.district.region.pk if instance.district.region else None,
            'name_ru': instance.district.region.name_ru if instance.district.region else None,
            'name_ky': instance.district.region.name_ky if instance.district.region else None,
            'name_en': instance.district.region.name_en if instance.district.region else None,
            'code_soato': instance.district.region.code_soato if instance.district.region else None,

        }

        representation['district'] = {
            'id': instance.district.pk if instance.district else None,
            'name_ru': instance.district.name_ru if instance.district else None,
            'name_ky': instance.district.name_ky if instance.district else None,
            'name_en': instance.district.name_en if instance.district else None,
            'code_soato': instance.district.code_soato if instance.district else None,
        }

        return representation


class UpdateContour_AISerializer(serializers.ModelSerializer):

    class Meta:
        model = Contour_AI
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['region_id'] = instance.conton.district.region.pk if instance.conton.district.region else None
        representation['district_id'] = instance.conton.district.pk if instance.conton.district else None

        return representation

    def is_polygon_inside_Kyrgyzstan(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT ST_Contains('{contour_Kyrgyzstan}'::geography::geometry, '{request}'::geography::geometry);
            """)
            inside = cursor.fetchall()
        return inside[0][0]

    def get_district(self, attrs):
        with connection.cursor() as cursor:
            cursor.execute(f"""
            SELECT dst.id FROM gip_district AS dst WHERE ST_Contains(dst.polygon::geography::geometry,
            '{attrs['polygon']}'::geography::geometry);
            """)
            district = cursor.fetchall()
        return district[0][0]

    def get_db_district(self, attrs):
        db_district = [i.district.pk if i.district else None for i in Conton.objects.filter(id=attrs['conton'].pk)]
        return db_district[0]

    def validate_district(self, attrs):
        district = self.get_district(attrs)
        db_district = self.get_db_district(attrs)
        if district != db_district:
            raise APIException({
                "message": f"Ваш контур выходит за пределы <{attrs['conton']}>"
            })

    def is_valid_year(self, attrs):
        if int(attrs['year']) > datetime.date.today().year:
            raise APIException({"message": "Год не может быть больше текущего года"})
        elif int(attrs['year']) < 2010:
            raise APIException({"message": "Год должен быть не менее 2010 года"})

    # def is_polygon_intersect(self, attrs):
    #     intersect = Contour_AI.objects.filter(
    #         polygon__intersects=attrs['polygon'], is_deleted=False, year=attrs['year'])
    #     if intersect:
    #         raise APIException({"message": "Пересекаются поля"})

    def validate(self, attrs):
        if not self.is_polygon_inside_Kyrgyzstan(attrs['polygon']):
            raise APIException({"message": "Создайте поле внутри Кыргызстана"})

        self.validate_district(attrs)

        self.is_valid_year(attrs)

        # self.is_polygon_intersect(attrs)

        return attrs
