from threading import Thread
from django.db import connection
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

# API view for generating a pivot table based on culture
class PivotTableCulture(APIView):
    def get(self, request):
        # Get the 'culture' parameter from the request query string
        culture = request.GET.get('culture')
        
        if culture:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    -- SQL Query to generate the pivot table data based on culture
                    """)
                rows = cursor.fetchall()
            
            # Format the query results into a JSON response
            data = []
            for i in rows:
                data.append({
                    'district_id': i[0],
                    'culture_id': i[1],
                    'max_elevation': i[2],
                    'min_elevation': i[3],
                    'ndvi_max': i[4],
                    'ndvi_min': i[5],
                    'vari_max': i[6],
                    'vari_min': i[7],
                    'ndwi_max': i[8],
                    'ndwi_min': i[9],
                    'ndre_max': i[10],
                    'ndre_min': i[11],
                    'savi_max': i[12],
                    'savi_min': i[13],
                    'district_name_en': i[14],
                    'district_name_ru': i[15],
                    'district_name_kg': i[16],
                    'year': '2022'  # You may need to change this year based on your requirement
                })
                
            return Response(data)
        else:
            return Response(data={"message": "parameter 'culture' is required"}, status=400)
