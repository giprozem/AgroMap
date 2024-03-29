from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView


class GraphicTablesAPIView(APIView):

    def get(self, request):
        """
        ?culture=id

        Обязательные поля:
        ?culture=id
        """
        culture = request.GET.get('culture')

        if not culture:
            return Response(data={"message": "parameter 'culture' is required"}, status=400)
        else:
            with connection.cursor() as cursor:
                cols = "year, culture_name, region_name, cy_sum, previous_year, difference"
                col_lst = cols.split(", ")
                cursor.execute(f"""with cte as (select rgn.name as region_name, cy.year as year, cl.name as culture_name,
                               round(sum(cntr.area_ha * cl.coefficient_crop)::numeric, 2) as cy_sum
                               from gip_contour as cntr
                               join gip_cropyield as cy
                               on cntr.id = cy.contour_id
                               join gip_culture as cl
                               on cl.id = cy.culture_id
                               join gip_conton as cntn
                               on cntn.id = cntr.conton_id
                               join gip_district as dst
                               on dst.id = cntn.district_id
                               join gip_region as rgn
                               on rgn.id = dst.region_id
                               group by cy.year, cl.id, rgn.id
                               having cl.id='{culture}'),
                               cte2 as (select region_name, year, culture_name, cy_sum, lag(cy_sum)
                               over(partition by region_name order by region_name, year) previous_year from cte)
                               select region_name, year, cy_sum, (cy_sum - previous_year) difference from cte2;""")
                rows = cursor.fetchall()
                datas = []
                for i in rows:
                    name = i[0]
                    data = list(i)[2:]
                    datas.append({"region_name": name, "source": data})

                formated_data = [{
                    "years": list(dict.fromkeys([row[1] for row in rows])),
                    "sources": [col_lst],
                    "data": datas

                }, ]
                return Response(formated_data)


class CulturePercentAPIView(APIView):
    def get(self, request):
        """
        Обязательные поля:
        ?year=int
        опциональные поля:
        ?region=id
        ?district=d
        """
        year = request.GET.get('year')
        region = request.GET.get('region')
        district = request.GET.get('district')

        if not year:
            return Response(data={"message": "parameter 'year' is required"}, status=400)
        else:
            if region:
                with connection.cursor() as cursor:
                    cursor.execute(f"""select cy.year, cl.name as culture_name, rgn.name as region_name, 
                                       round(sum(cntr.area_ha * cl.coefficient_crop)::numeric, 2) as sum
                                       from gip_contour as cntr
                                       join gip_cropyield as cy 
                                       on cntr.id = cy.contour_id
                                       join gip_culture as cl
                                       on cl.id = cy.culture_id 
                                       join gip_conton as cntn 
                                       on cntn.id = cntr.conton_id 
                                       join gip_district as dst 
                                       on dst.id = cntn.district_id 
                                       join gip_region as rgn 
                                       on rgn.id = dst.region_id  
                                       group by cy.year, rgn.id, cl.id
                                       having cy.year='{year}' and rgn.id='{region}'""")
                    rows = cursor.fetchall()
                    formated_data = {
                        "cultures": [row[1] for row in rows],
                        "values": [row[-1] for row in rows]
                    }
                    return Response(formated_data)

            elif district:
                with connection.cursor() as cursor:
                    cursor.execute(f"""select cy.year, cl.name as culture_name, dst.name as district_name, 
                                       round(sum(cntr.area_ha * cl.coefficient_crop)::numeric, 2) as sum
                                       from gip_contour as cntr
                                       join gip_cropyield as cy 
                                       on cntr.id = cy.contour_id
                                       join gip_culture as cl
                                       on cl.id = cy.culture_id 
                                       join gip_conton as cntn 
                                       on cntn.id = cntr.conton_id 
                                       join gip_district as dst 
                                       on dst.id = cntn.district_id 
                                       group by cy.year, dst.id, cl.id
                                       having cy.year='{year}' and dst.id='{district}'""")
                    rows = cursor.fetchall()
                    formated_data = {
                        "cultures": [row[1] for row in rows],
                        "values": [row[-1] for row in rows]
                    }
                return Response(formated_data)
            else:
                with connection.cursor() as cursor:
                    cursor.execute(f"""select cy.year, cl.name as culture_name, 
                                       round(sum(cntr.area_ha * cl.coefficient_crop)::numeric, 2) as sum
                                       from gip_contour as cntr
                                       join gip_cropyield as cy 
                                       on cntr.id = cy.contour_id
                                       join gip_culture as cl
                                       on cl.id = cy.culture_id 
                                       join gip_conton as cntn 
                                       on cntn.id = cntr.conton_id 
                                       join gip_district as dst 
                                       on dst.id = cntn.district_id 
                                       group by cy.year, cl.id
                                       having cy.year='{year}'""")
                    rows = cursor.fetchall()
                    formated_data = {
                        "cultures": [row[1] for row in rows],
                        "values": [row[-1] for row in rows]
                    }
                return Response(formated_data)
