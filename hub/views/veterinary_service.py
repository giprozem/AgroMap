import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import District, Conton


class AmountCattleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        district_id = request.GET.get('district')
        conton_id = request.GET.get('conton')
        if district_id and conton_id:
            conton = Conton.objects.filter(district_id=district_id, id=conton_id)
            code_soato = conton.values_list('code_soato')[0][0] if conton else None
            if code_soato is not None:
                response = requests.get(f'https://aitstest.gvfi.gov.kg/api/data/all?id={code_soato}').json()
                return Response(response)
            else:
                return Response({
                    "total": "0",
                    "active": "0",
                    "notActive": "0",
                    "totalObjects": "0",
                    "totalSubjects": "0"
                })
        elif district_id:
            district = District.objects.filter(id=district_id)
            code_soato = district.values_list('code_soato')[0][0] if district else None
            if code_soato is not None:
                response = requests.get(f'https://aitstest.gvfi.gov.kg/api/data/all?id={code_soato}').json()
                return Response(response)
            else:
                return Response({
                    "total": "0",
                    "active": "0",
                    "notActive": "0",
                    "totalObjects": "0",
                    "totalSubjects": "0"
                })
        elif conton_id:
            conton = Conton.objects.filter(id=conton_id)
            code_soato = conton.values_list('code_soato')[0][0] if conton else None
            if code_soato is not None:
                response = requests.get(f'https://aitstest.gvfi.gov.kg/api/data/all?id={code_soato}').json()
                return Response(response)
            else:
                return Response({
                    "total": "0",
                    "active": "0",
                    "notActive": "0",
                    "totalObjects": "0",
                    "totalSubjects": "0"
                })
        else:
            return Response(data={"message": "parameter 'district or conton' is required"}, status=400)
