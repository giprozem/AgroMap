from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from hub.models import LandInfo


class ZemBalanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = LandInfo
        fields = '__all__'


class LandInfoSerializers(GeoFeatureModelSerializer):
    class Meta:
        model = LandInfo
        fields = '__all__'
        geo_field = 'main_map'


class LandInfoCustomSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandInfo
        fields = ('ink_code', )

# class InfoPlotSerializers(GeoFeatureModelSerializer):
#     class Meta:
#         model = LandInfo
#         fields = ('id', 'ink_code', 'eni_code', 'asr_address', 'longitude', 'latitude', 'owner_info', 'inn_pin',
#                   'property_form', 'doc_enttitlement', 'special_purpose_asr', 'land_factarea_asr')
#         geo_field = 'main_map'