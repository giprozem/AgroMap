import datetime

from django.contrib.gis.geos import GEOSGeometry
from django.db import connection
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from gip.models import CropYield, District
from gip.models.conton import Conton
from gip.models.contour import Contour, LandType
from gip.views.handbook_contour import contour_Kyrgyzstan
from rest_framework.validators import UniqueValidator


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


class LandTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandType
        exclude = ('name',)


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
        # representation['properties'] = {'created_at': instance.created_at, 'updated_at': instance.updated_at,
        #                                 'ink': instance.ink, 'code_soato': instance.code_soato,
        #                                 'year': instance.year, 'area_ha': instance.area_ha,
        #                                 'conton': instance.conton.pk,
        #                                 'farmer': instance.farmer.pk if instance.farmer else None,
        #                                 'district': instance.conton.district.pk if instance.conton.district else None,
        #                                 'region': instance.conton.district.region.pk if instance.conton.district.region else None,
        #                                 'productivity': instance.productivity,
        #                                 'culture': instance.culture.pk if instance.culture else None,
        #                                 'type': instance.type.pk, 'is_deleted': instance.is_deleted,
        #                                 'elevation': instance.elevation, 'is_rounded': instance.is_rounded
        #                                 }
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
            raise ValidationError({
                "district": f"Ваш контур выходит за пределы <{attrs['conton']}>"
            })

    def is_valid_year(self, attrs):
        if int(attrs['year']) > datetime.date.today().year:
            raise ValidationError({"year": "Год не может быть больше текущего года"})
        elif int(attrs['year']) < 2010:
            raise ValidationError({"year": "Год должен быть не менее 2010 года"})

    def is_polygon_intersect(self, attrs):
        intersect = Contour.objects.filter(
            polygon__intersects=attrs['polygon'], is_deleted=False, year=attrs['year'])
        if intersect:
            raise ValidationError({"polygon": "Пересекаются поля"})

    def validate(self, attrs):
        if not self.is_polygon_inside_Kyrgyzstan(attrs['polygon']):
            raise ValidationError({"polygon": "Создайте поле внутри Кыргызстана"})

        self.validate_district(attrs)

        self.is_valid_year(attrs)

        self.is_polygon_intersect(attrs)

        return attrs
