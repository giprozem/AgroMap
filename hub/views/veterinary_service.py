"""
veterinary_service.py:
This module contains views to fetch data related to veterinary services based on district and conton.

Classes:
- `AmountCattleAPIView`: Handles the retrieval of cattle data based on district and conton.
    Methods:
        - `get`: Processes GET requests. Retrieves the total number of cattle based on the provided district and/or conton.
"""

import requests
from decouple import config
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import District, Conton

VET_SERVICE_URL = config('VET_SERVICE_URL')


class AmountCattleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        district_id = request.GET.get('district')  # Retrieve district ID from request
        conton_id = request.GET.get('conton')  # Retrieve conton ID from request

        if district_id and conton_id:
            conton = Conton.objects.filter(district_id=district_id, id=conton_id)
            code_soato = conton.values_list('code_soato_vet')[0][0] if conton else None
            if code_soato is not None:
                response = requests.get(f'{VET_SERVICE_URL}={code_soato}').json()
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
            code_soato = district.values_list('code_soato_vet')[0][0] if district else None
            print(district.values_list('code_soato_vet'))
            if code_soato is not None:
                response = requests.get(f'{VET_SERVICE_URL}={code_soato}').json()
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
            code_soato = conton.values_list('code_soato_vet')[0][0] if conton else None
            if code_soato is not None:
                response = requests.get(f'{VET_SERVICE_URL}={code_soato}').json()
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
