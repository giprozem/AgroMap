"""
land_info.py:
This module handles operations related to the `LandInfo` model.

Classes:
- `LandInfoViewSet`: Provides CRUD operations for `LandInfo` objects.
    Attributes:
        - `queryset`: Retrieves all the `LandInfo` objects.
        - `serializer_class`: Serializer used to handle `LandInfo` instances.
        - `lookup_field`: The field used to look up a `LandInfo` object.

- `LandInfoSearch`: Handles the search functionality for `LandInfo` based on `ink_code`.
    Methods:
        - `get`: Processes GET requests. If a search term is provided, it filters `LandInfo` objects based on the `ink_code`
          containing the search term.
"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from hub.models import LandInfo
from hub.serializers.land_info import LandInfoSerializers, LandInfoCustomSearchSerializer


class LandInfoViewSet(viewsets.ModelViewSet):
    queryset = LandInfo.objects.all()  # All LandInfo instances from the database
    serializer_class = LandInfoSerializers  # Serializer to handle LandInfo objects
    lookup_field = 'ink_code'  # Field used for lookup


class LandInfoSearch(APIView):
    def get(self, request, *args, **kwargs):
        search = request.GET.get('search', '')  # Retrieve the search query from request
        land_info = LandInfo.objects.all()
        if search:
            ink_code = land_info.filter(ink_code__icontains=search)  # Filter LandInfo by ink_code
            return Response({"list_ink_code": LandInfoCustomSearchSerializer(ink_code, many=True).data})
        return Response([])
