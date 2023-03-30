from rest_framework import serializers
from ai.models.predicted_contour import Contour_AI


class Contour_AISerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour_AI
        fields = ('culture', 'conton_id', 'district_id', 'polygon' )

    # def is_polygon_inside_Kyrgyzstan(self, request, *args, **kwargs):
    #     with connection.cursor() as cursor:
    #         cursor.execute(f"""
    #             SELECT ST_Contains('{contour_Kyrgyzstan}'::geography::geometry, '{request}'::geography::geometry);
    #         """)
    #         inside = cursor.fetchall()
    #     return inside[0][0]
    #
    # def validate(self, attrs):
    #     if not self.is_polygon_inside_Kyrgyzstan(attrs['polygon']):
    #         raise APIException({"message": "Создайте поле внутри Кыргызстана"})
    #     return attrs
