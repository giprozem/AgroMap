import datetime

from django.db import connection
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueValidator

from gip.models import CropYield
from gip.models.conton import Conton
from gip.models.contour import Contour
from gip.serializers.conton import ContonWithoutPolygonSerializer
from gip.serializers.culture import CultureSerializer
from gip.serializers.landtype import LandTypeSerializer
from gip.serializers.soil import SoilClassSerializer
from gip.views.handbook_contour import contour_Kyrgyzstan


class ContonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conton
        fields = ('polygon',)


class ContourAutocompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = ('polygon',)


class CalculatePolygonContourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = '__all__'


class CropYieldInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropYield
        fields = ('id', 'year', 'culture')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['culture'] = instance.culture.name
        return representation


class ContourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = '__all__'


class UpdateAuthDetailContourSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(required=True)
    code_soato = serializers.CharField(
        max_length=30, required=False,
        validators=[UniqueValidator(queryset=Contour.objects.all().filter(is_deleted=False),
                                    message=(
                                        "C таким Код территории по СОАТО уже существует в базе"))]
    )

    ink = serializers.CharField(
        max_length=30, required=False,
        validators=[UniqueValidator(queryset=Contour.objects.all().filter(is_deleted=False),
                                    message=(
                                        "C таким Идентификационный номер контура уже существует в базе"))]
    )

    class Meta:
        model = Contour
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['region_id'] = instance.conton.district.region.pk if instance.conton.district.region else None
        representation['district_id'] = instance.conton.district.pk if instance.conton.district else None

        return representation


class AuthDetailContourSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(required=True)
    code_soato = serializers.CharField(
        max_length=30, required=False,
        validators=[UniqueValidator(queryset=Contour.objects.all().filter(is_deleted=False),
                                    message=(
                                        "C таким Код территории по СОАТО уже существует в базе"))]
    )

    ink = serializers.CharField(
        max_length=30, required=False,
        validators=[UniqueValidator(queryset=Contour.objects.all().filter(is_deleted=False),
                                    message=(
                                        "C таким Идентификационный номер контура уже существует в базе"))]
    )

    class Meta:
        model = Contour
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['region'] = {
            'id': instance.conton.district.region.pk if instance.conton.district.region else None,
            'name_ru': instance.conton.district.region.name_ru if instance.conton.district.region else None,
            'name_ky': instance.conton.district.region.name_ky if instance.conton.district.region else None,
            'name_en': instance.conton.district.region.name_en if instance.conton.district.region else None,
            'code_soato': instance.conton.district.region.code_soato if instance.conton.district.region else None
        }
        representation['district'] = {
            'id': instance.conton.district.pk if instance.conton.district else None,
            'name_ru': instance.conton.district.name_ru if instance.conton.district else None,
            'name_ky': instance.conton.district.name_ky if instance.conton.district else None,
            'name_en': instance.conton.district.name_en if instance.conton.district else None,
            'code_soato': instance.conton.district.code_soato if instance.conton.district else None
        }
        representation['conton'] = {
            'id': instance.conton.pk if instance.conton else None,
            'name_ru': instance.conton.name_ru if instance.conton else None,
            'name_ky': instance.conton.name_ky if instance.conton else None,
            'name_en': instance.conton.name_en if instance.conton else None,
            'code_soato': instance.conton.code_soato if instance.conton.district else None
        }
        representation['soil_class'] = {
            'id': instance.soil_class.pk if instance.soil_class else None,
            'ID': instance.soil_class.ID if instance.soil_class else None,
            'name_ru': instance.soil_class.name_ru if instance.soil_class else None,
            'name_ky': instance.soil_class.name_ky if instance.soil_class else None,
            'name_en': instance.soil_class.name_en if instance.soil_class else None,
            'description_ru': instance.soil_class.description_ru if instance.soil_class else None,
            'description_ky': instance.soil_class.description_ky if instance.soil_class else None,
            'description_en': instance.soil_class.description_en if instance.soil_class else None,
            'color': instance.soil_class.color if instance.soil_class else None
        }
        representation['type'] = {
            'id': instance.type.pk if instance.type else None,
            'name_ru': instance.type.name_ru if instance.type else None,
            'name_ky': instance.type.name_ky if instance.type else None,
            'name_en': instance.type.name_en if instance.type else None
        }
        representation['culture'] = {
            'id': instance.culture.pk if instance.culture else None,
            'name_ru': instance.culture.name_ru if instance.culture else None,
            'name_ky': instance.culture.name_ky if instance.culture else None,
            'name_en': instance.culture.name_en if instance.culture else None,
            'coefficient_crop': instance.culture.coefficient_crop if instance.culture else None
        }
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

    def is_polygon_intersect(self, attrs):
        intersect = Contour.objects.filter(
            polygon__intersects=attrs['polygon'], is_deleted=False, year=attrs['year'])
        if intersect:
            raise APIException({"message": "Пересекаются поля"})

    def validate(self, attrs):
        if not self.is_polygon_inside_Kyrgyzstan(attrs['polygon']):
            raise APIException({"message": "Создайте поле внутри Кыргызстана"})

        self.validate_district(attrs)

        self.is_valid_year(attrs)

        self.is_polygon_intersect(attrs)

        return attrs
