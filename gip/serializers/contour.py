import datetime

from django.contrib.gis.geos import GEOSGeometry
from django.db import connection
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from gip.models import CropYield
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


# class ContourYearSerializer(GeoFeatureModelSerializer):
#     class Meta:
#         model = ContourYear
#         fields = '__all__'
#         geo_field = 'polygon'


class LandTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandType
        exclude = ('name',)


class AuthDetailContourSerializer(GeoFeatureModelSerializer):
    year = serializers.IntegerField(required=True)
    code_soato = serializers.CharField(
        max_length=30,
        validators=[UniqueValidator(queryset=Contour.objects.all(),
                                    message=(
                                        "C таким Код территории по СОАТО уже существует в базе"))]
    )

    ink = serializers.CharField(
        max_length=30,
        validators=[UniqueValidator(queryset=Contour.objects.all(),
                                    message=(
                                        "C таким Идентификационный номер контура уже существует в базе"))]
    )

    class Meta:
        model = Contour
        fields = '__all__'
        geo_field = 'polygon'

    def validate(self, attrs):
        with connection.cursor() as cursor:
            cursor.execute(f"""
            SELECT ST_Contains('{contour_Kyrgyzstan}'::geography::geometry, '{attrs['polygon']}'::geography::geometry);
            """)
            inside = cursor.fetchall()
        intersect = Contour.objects.filter(
            polygon__intersects=attrs['polygon'], is_deleted=False)
        if int(attrs['year']) > datetime.date.today().year:
            raise ValidationError({"year": "Год не может быть больше текущего года"})
        elif int(attrs['year']) < 2010:
            raise ValidationError({"year": "Год должен быть не менее 2010 года"})
        elif not inside[0][0]:
            raise ValidationError({"polygon": "Создайте поле внутри Кыргызстана"})
        elif intersect:
            raise ValidationError({"polygon": "Пересекаются поля"})
        return attrs
