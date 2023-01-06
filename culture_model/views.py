from django.db import connection
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


class IndexPlanWithAPIView(APIView):
    def get(self, request):
        """
        ?culture=id=id&region

        Обязательные поля:
        ?culture=id

        Необязательные поля:
        region=id
        """
        culture = request.GET.get('culture')
        region = request.GET.get('region')
        if not culture:
            return Response(data={"message": "parameter 'culture' is required"}, status=400)
        else:
            if region:
                with connection.cursor() as cursor:
                    cursor.execute(f"""with cte as (select rgn.name as region, cmip.value as value, 
                                   clt.name as culture_name, dcd.start_date as start_date, dcd.end_date as end_date
                                   from culture_model_indexplan as cmip
                                   join gip_culture as clt on clt.id=cmip.culture_id
                                   join gip_region as rgn on rgn.id=cmip.region_id
                                   join culture_model_decade as dcd on dcd.id=cmip.decade_id
                                   where clt.id={culture} and rgn.id={region}),
                                   cte2 as (select region, start_date, end_date, value, lag(value)  
                                   over() previous_value  from cte)
                                   select region, start_date, end_date, value, (value - previous_value) difference from cte2;
                    """)
                    rows = cursor.fetchall()
                    formated_data = {
                        "decade": [row[1] for row in rows],
                        "data": [row[-2] for row in rows]
                    }
                return Response(formated_data)
