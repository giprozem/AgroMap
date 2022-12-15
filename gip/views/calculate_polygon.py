from django.http import HttpResponse
from rest_framework import status
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
                    cols = "cntr.id, cy.year, cl.name, cntr.sum_ha, cl.coefficient_crop, " \
                           "cntr.sum_ha * cl.coefficient_crop as crop"
                    col_lst = cols.split(", ")
                    cursor.execute(f"""select cy.year, cl.name, rgn.name, 
                                   round(sum(cntr.sum_ha * cl.coefficient_crop)::numeric, 2) as cy_sum
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
                                   having rgn.id='{region}' and cl.id='{culture}'
                                   order by cy.year""")
                    rows = cursor.fetchall()
                    formated_data = {
                        "years": [row[0] for row in rows],
                        "crop": [row[-1] for row in rows],
                        "source": [col_lst] + rows
                    }
                return Response(formated_data)

            elif district:
                with connection.cursor() as cursor:
                    cols = "cntr.id, cy.year, cl.name, cntr.sum_ha, cl.coefficient_crop, " \
                           "cntr.sum_ha * cl.coefficient_crop as crop"
                    col_lst = cols.split(", ")
                    cursor.execute(f"""select cy.year, cl.name, dst.name, 
                                   round(sum(cntr.sum_ha * cl.coefficient_crop)::numeric, 2) as cy_sum
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
                                   having dst.id='{district}' and cl.id='{culture}'
                                   order by cy.year""")
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
                    cursor.execute(f"""select cy.year, cl.name, cntn.name, 
                                   round(sum(cntr.sum_ha * cl.coefficient_crop)::numeric, 2) as cy_sum
                                   from gip_contour as cntr
                                   join gip_cropyield as cy 
                                   on cntr.id = cy.contour_id
                                   join gip_culture as cl
                                   on cl.id = cy.culture_id 
                                   join gip_conton as cntn 
                                   on cntn.id = cntr.conton_id 
                                   group by cy.year, cntn.id, cl.id
                                   having cntn.id='{conton}' and cl.id='{culture}'
                                   order by cy.year""")
                    rows = cursor.fetchall()
                    formated_data = {
                        "years": [row[0] for row in rows],
                        "crop": [row[-1] for row in rows],
                        "source": [col_lst] + rows
                    }
                return Response(formated_data)


            else:
                with connection.cursor() as cursor:
                    cursor.execute(f"""select cy.year, cl.name, 
                                   round(sum(cntr.sum_ha * cl.coefficient_crop)::numeric, 2) as cy_sum
                                   from gip_contour as cntr
                                   join gip_cropyield as cy 
                                   on cntr.id = cy.contour_id
                                   join gip_culture as cl
                                   on cl.id = cy.culture_id 
                                   join gip_conton as cntn 
                                   on cntn.id = cntr.conton_id
                                   group by cy.year, cl.id
                                   having cl.id=1
                                   order by cy.year""")
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
                               round(sum(cntr.sum_ha * cl.coefficient_crop)::numeric, 2) as cy_sum
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
                               select region_name, year, cy_sum, (previous_year - cy_sum) difference from cte2;""")
                rows = cursor.fetchall()
                datas = []
                for i in rows:
                    name = i[0]
                    data = list(i)[2:]
                    print(data)
                    datas.append({"region_name": name, "source": data})


                formated_data = [{
                    "years": list(dict.fromkeys([row[1] for row in rows])),
                    "sources": [col_lst],
                    "data": datas

                }, ]
                return Response(formated_data)