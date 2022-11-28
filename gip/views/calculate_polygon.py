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
                    cols = "cntr.id, cy.year, cl.name, cntr.sum_ha, cl.coefficient_crop, " \
                           "cntr.sum_ha * cl.coefficient_crop as crop"
                    col_lst = cols.split(", ")
                    cursor.execute(f"""select cy.year, cl.name, rgn.name, sum(cntr.sum_ha * cl.coefficient_crop) as cy_sum
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
                    cursor.execute(f"""select cy.year, cl.name, dst.name, sum(cntr.sum_ha * cl.coefficient_crop) as cy_sum
                                   from gip_contour as cntr
                                   join gip_cropyield as cy 
                                   on cntr.id = cy.contour_id
                                   join gip_culture as cl
                                   on cl.id = cy.culture_id \
                                   join gip_conton as cntn 
                                   on cntn.id = cntr.conton_id 
                                   join gip_district as dst 
                                   on dst.id = cntn.district_id  
                                   group by cy.year, cl.id, dst.id 
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
                    cols = "cntr.id, cy.year, cl.name, cntr.sum_ha, cl.coefficient_crop, " \
                           "cntr.sum_ha * cl.coefficient_crop as crop"
                    col_lst = cols.split(", ")
                    cursor.execute(f"""select cy.year, cl.name, cntn.name, sum(cntr.sum_ha * cl.coefficient_crop) as cy_sum
                                   from gip_contour as cntr
                                   join gip_cropyield as cy 
                                   on cntr.id = cy.contour_id
                                   join gip_culture as cl
                                   on cl.id = cy.culture_id 
                                   join gip_conton as cntn on 
                                   cntn.id = cntr.conton_id  
                                   group by cy.year, cl.id, cntn.id
                                   having cntn.id={conton} and cl.id='{culture}'
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
                    cursor.execute(f"""select cy.year, cl.name, sum(cntr.sum_ha * cl.coefficient_crop) as cy_sum
                                   from gip_contour as cntr
                                   join gip_cropyield as cy 
                                   on cntr.id = cy.contour_id
                                   join gip_culture as cl
                                   on cl.id = cy.culture_id
                                   join gip_conton as cntn 
                                   on cntn.id = cntr.conton_id
                                   group by cy.year, cl.id
                                   having cl.id={culture}
                                   order by cy.year""")
                    rows = cursor.fetchall()
                    formated_data = {
                        "years": [row[0] for row in rows],
                        "crop": [row[-1] for row in rows],
                        "source": [["year", "cy_sum"]] + rows
                    }
                return Response(formated_data)

