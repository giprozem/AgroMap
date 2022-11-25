from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response


class StatisticsAPIView(APIView):

    def get(self, request):
        culture = request.GET.get('culture')
        conton = request.GET.get('conton')
        district = request.GET.get('district')
        region = request.GET.get('region')

        if conton:
            with connection.cursor() as cursor:
                cols = "cntr.id, cy.year, cl.name, cntr.sum_ha, cl.coefficient_crop, " \
                       "cntr.sum_ha * cl.coefficient_crop as crop"
                col_lst = cols.split(", ")
                cursor.execute(f"""select cy.year, sum(cntr.sum_ha * cl.coefficient_crop) as cy_sum
                               from gip_contour as cntr
                               join gip_cropyield as cy 
                               on cntr.id = cy.contour_id
                               join gip_culture as cl
                               on cl.id = cy.culture_id join gip_conton as cntn on cntn.id = cntr.conton_id  
                               where cntn.id={conton} and cl.name='{culture}' group by cy.year order by cy.year""")
                rows = cursor.fetchall()
            return Response([col_lst] + rows)
        elif district:
            with connection.cursor() as cursor:
                cols = "cntr.id, cy.year, cl.name, cntr.sum_ha, cl.coefficient_crop, " \
                       "cntr.sum_ha * cl.coefficient_crop as crop"
                col_lst = cols.split(", ")
                cursor.execute(f"""select cy.year, sum(cntr.sum_ha * cl.coefficient_crop) as cy_sum
                               from gip_contour as cntr
                               join gip_cropyield as cy 
                               on cntr.id = cy.contour_id
                               join gip_culture as cl
                               on cl.id = cy.culture_id join gip_conton as cntn on cntn.id = cntr.conton_id 
                               join gip_district as dst on dst.id = cntn.district_id  
                               where dst.id='{district}' and cl.name='{culture}' group by cy.year order by cy.year""")
                rows = cursor.fetchall()
            return Response([col_lst] + rows)
        elif region:
            with connection.cursor() as cursor:
                cols = "cntr.id, cy.year, cl.name, cntr.sum_ha, cl.coefficient_crop, " \
                       "cntr.sum_ha * cl.coefficient_crop as crop"
                col_lst = cols.split(", ")
                cursor.execute(f"""select cy.year, sum(cntr.sum_ha * cl.coefficient_crop) as cy_sum
                               from gip_contour as cntr
                               join gip_cropyield as cy 
                               on cntr.id = cy.contour_id
                               join gip_culture as cl
                               on cl.id = cy.culture_id join gip_conton as cntn on cntn.id = cntr.conton_id 
                               join gip_district as dst on dst.id = cntn.district_id 
                               join gip_region as rgn on rgn.id = dst.region_id  
                               where rgn.id='{region}' and cl.name='{culture}' group by cy.year order by cy.year""")
                rows = cursor.fetchall()
            return Response([col_lst] + rows)

        else:
            with connection.cursor() as cursor:
                cursor.execute(f"""select cy.year, sum(cntr.sum_ha * cl.coefficient_crop) as cy_sum
                               from gip_contour as cntr
                               join gip_cropyield as cy 
                               on cntr.id = cy.contour_id
                               join gip_culture as cl
                               on cl.id = cy.culture_id
                               join gip_conton as cntn on cntn.id = cntr.conton_id group by cy.year order by cy.year""")
                rows = cursor.fetchall()
            return Response([["year", "cy_sum"]] + rows)
