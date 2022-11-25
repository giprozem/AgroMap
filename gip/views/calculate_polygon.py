from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response


class StatisticsAPIView(APIView):

    def get(self, request):

        with connection.cursor() as cursor:
            cols = "cntr.id, cy.year, cl.name, cntr.sum_ha, cl.coefficient_crop, cntr.sum_ha * cl.coefficient_crop as crop"
            col_lst = cols.split(", ")
            cursor.execute(f"""
                select cntr.id, cy.year, cl.name, cntr.sum_ha, cl.coefficient_crop, cntr.sum_ha * cl.coefficient_crop as crop
                from gip_contour as cntr
                join gip_cropyield as cy 
                on cntr.id = cy.contour_id
                join gip_culture as cl
                on cl.id = cy.culture_id
            ;""")
            rows = cursor.fetchall()
        return Response([col_lst] + rows)
