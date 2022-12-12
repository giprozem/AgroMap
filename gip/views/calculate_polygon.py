from django.http import HttpResponse
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response


class StatisticsAPIView(APIView):

    def get(self, request):
        """

        ?region=id&culture=id

        Обязательные поля:
        ?culture=id

        Необязательные поля:
        region=id
        district=id
        conton=id

        """
        culture = request.GET.get('culture')
        conton = request.GET.get('conton')
        district = request.GET.get('district')
        region = request.GET.get('region')

        if not culture:
            return Response(data={"message": "parameter 'culture' is required"}, status=400)
        else:
            if region:
                with connection.cursor() as cursor:
                    cols = "year, culture_name, region_name, cy_sum, previous_year, difference"
                    col_lst = cols.split(", ")
                    cursor.execute(f"""with cte as (select cy.year, cl.name as culture_name, rgn.name as region_name, 
                                   sum(cntr.sum_ha * cl.coefficient_crop) as cy_sum
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
                                   having rgn.id='{region}' and cl.id='{culture}'), 
                                   cte2 as (select year, culture_name, region_name, cy_sum, lag(cy_sum,1) 
                                   over(order by year) previous_year from cte) 
                                   select *, (previous_year - cy_sum) difference from cte2;""")
                    rows = cursor.fetchall()
                    formated_data = {
                        "years": [row[0] for row in rows],
                        "crop": [row[-1] for row in rows],
                        "source": [col_lst] + rows
                    }
                return Response(formated_data)

            elif district:
                with connection.cursor() as cursor:
                    cols = "year, culture_name, district_name, cy_sum, previous_year, difference"
                    col_lst = cols.split(", ")
                    cursor.execute(f"""with cte as (select cy.year, cl.name as culture_name, dst.name as district_name, 
                                   sum(cntr.sum_ha * cl.coefficient_crop) as cy_sum
                                   from gip_contour as cntr
                                   join gip_cropyield as cy 
                                   on cntr.id = cy.contour_id
                                   join gip_culture as cl
                                   on cl.id = cy.culture_id 
                                   join gip_conton as cntn 
                                   on cntn.id = cntr.conton_id 
                                   join gip_district as dst 
                                   on dst.id = cntn.district_id  
                                   group by cy.year, cl.id, dst.id 
                                   having dst.id='{district}' and cl.id='{culture}'), 
                                   cte2 as (select year, culture_name, district_name, cy_sum, lag(cy_sum,1) 
                                   over(order by year) previous_year from cte) 
                                   select *, (previous_year - cy_sum) difference from cte2;""")
                    rows = cursor.fetchall()
                    formated_data = {
                        "years": [row[0] for row in rows],
                        "crop": [row[-1] for row in rows],
                        "source": [col_lst] + rows
                    }
                return Response(formated_data)

            elif conton:
                with connection.cursor() as cursor:
                    cols = "year, culture_name, conton_name, cy_sum, previous_year, difference"
                    col_lst = cols.split(", ")
                    cursor.execute(f"""with cte as (select cy.year, cl.name as culture_name, cntn.name as conton_name, 
                                   sum(cntr.sum_ha * cl.coefficient_crop) as cy_sum
                                   from gip_contour as cntr
                                   join gip_cropyield as cy 
                                   on cntr.id = cy.contour_id
                                   join gip_culture as cl
                                   on cl.id = cy.culture_id 
                                   join gip_conton as cntn 
                                   on cntn.id = cntr.conton_id 
                                   join gip_district as dst 
                                   on dst.id = cntn.district_id  
                                   group by cy.year, cl.id, cntn.id 
                                   having cntn.id='{conton}' and cl.id='{culture}'), 
                                   cte2 as (select year, culture_name, conton_name, cy_sum, lag(cy_sum,1) 
                                   over(order by year) previous_year from cte) 
                                   select *, (previous_year - cy_sum) difference from cte2;""")
                    rows = cursor.fetchall()
                    formated_data = {
                        "years": [row[0] for row in rows],
                        "crop": [row[-1] for row in rows],
                        "source": [col_lst] + rows
                    }
                return Response(formated_data)


            else:
                with connection.cursor() as cursor:
                    cursor.execute(f"""with cte as (select cy.year, cl.name as culture_name, 
                                   sum(cntr.sum_ha * cl.coefficient_crop) as cy_sum
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
                                   having cl.id='{culture}'), 
                                   select *, (previous_year - cy_sum) difference from cte2;""")
                    rows = cursor.fetchall()
                    formated_data = {
                        "years": [row[0] for row in rows],
                        "crop": [row[-1] for row in rows],
                        "source": [["year", "cy_sum"]] + rows
                    }
                return Response(formated_data)


class ContourCultureAPIView(APIView):

    def get(self, request):
        conton = request.GET.get('conton')
        ink = request.GET.get('ink')
        if conton:
            with connection.cursor() as cursor:
                cursor.execute(f"""select cntn.name, cntr.ink, cl.name, cntr.sum_ha, cy.year
                                   from gip_contour as cntr
                                   join gip_cropyield as cy 
                                   on cntr.id = cy.contour_id
                                   join gip_culture as cl
                                   on cl.id = cy.culture_id
                                   join gip_conton as cntn 
                                   on cntn.id = cntr.conton_id 
                                   where cntn.id={conton}
                                   order by -cy.year limit 1""")
                rows = cursor.fetchall()
            return Response(rows)

        elif ink:
            with connection.cursor() as cursor:
                cursor.execute(f"""select cntn.name, cntr.ink, cl.name, cntr.sum_ha, cy.year
                                   from gip_contour as cntr
                                   join gip_cropyield as cy 
                                   on cntr.id = cy.contour_id
                                   join gip_culture as cl
                                   on cl.id = cy.culture_id
                                   join gip_conton as cntn 
                                   on cntn.id = cntr.conton_id 
                                   where cntr.ink='{ink}' 
                                   order by -cy.year limit 1""")
                rows = cursor.fetchall()
            return Response(rows)
        else:
            with connection.cursor() as cursor:
                cursor.execute(f"""select cntn.name, cntr.ink, cl.name, cntr.sum_ha, cy.year
                                   from gip_contour as cntr
                                   join gip_cropyield as cy 
                                   on cntr.id = cy.contour_id
                                   join gip_culture as cl
                                   on cl.id = cy.culture_id
                                   join gip_conton as cntn 
                                   on cntn.id = cntr.conton_id""")
                rows = cursor.fetchall()
            return Response(rows)