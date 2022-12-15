from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView


class OwnerDetailsAPIView(APIView):
    def get(self, request):
        ink = request.GET.get('ink')
        pin_inn = request.GET.get('pin_inn')
        if pin_inn:
            with connection.cursor() as cursor:
                cursor.execute(f"""select cntr.ink, frmr.pin_inn 
                               from gip_contour as cntr 
                               join gip_farmer as frmr 
                               on frmr.id = cntr.farmer_id 
                               group by cntr.ink, frmr.pin_inn 
                               having frmr.pin_inn='{pin_inn}'""")
                rows = cursor.fetchall()
                formated_data = {
                    "pin_inn": list(dict.fromkeys([row[1] for row in rows])),
                    "ink": [row[0] for row in rows]
                }
                return Response(formated_data)
        elif ink:
            with connection.cursor() as cursor:
                cursor.execute(f"""select cntr.ink, cntr.polygon, cntr.sum_ha, frmr.pin_inn, cl.name as culture_name,
                                round(sum(cntr.sum_ha * cl.coefficient_crop)::numeric, 2) as cy_sum
                               from gip_contour as cntr 
                               join gip_farmer as frmr 
                               on frmr.id = cntr.farmer_id 
                               join gip_cropyield as cy
                               on cntr.id = cy.contour_id
                               join gip_culture as cl
                               on cl.id = cy.culture_id
                               group by cntr.ink, frmr.pin_inn, cntr.polygon, cntr.sum_ha, cl.name 
                               having cntr.ink='{ink}'""")
                rows = cursor.fetchall()
                formated_data = {
                    "ink": list(dict.fromkeys([row[0] for row in rows])),
                    "data": [row[1:] for row in rows]
                }
                return Response(formated_data)



