from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from gip.models import CropYield
from gip.models.conton import Conton
from gip.models.contour import Contour, LandType, ContourYear


class ContonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conton
        fields = ('polygon', )


class ContourAutocompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = ('polygon', )


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


class ContourYearSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ContourYear
        fields = '__all__'
        geo_field = 'polygon'


class LandTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandType
        exclude = ('name', )


class AuthDetailContourYearSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ContourYear
        fields = '__all__'
        geo_field = 'polygon'

    def validate_year(self, value):
        if int(value) < 2010:
            raise serializers.ValidationError("Год должен быть не менее 2010 года")
        return value

    def validate(self, data):
        if int(data['year']) > 2023:
            raise serializers.ValidationError("Год не может быть больше текущего года")
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['required'] = 'Это поле обязательно для заполнения'


class AuthDetailContourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = '__all__'
