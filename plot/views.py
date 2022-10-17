from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from plot.models import Plot, CultureField, Crop
from plot.serializers import PlotSerializer, CultureFieldSerializerInlinePost, CultureFieldSerializerInline, \
    CropSerializer


@method_decorator(csrf_exempt, name="dispatch")
class PlotViewSet(viewsets.ModelViewSet):
    queryset = Plot.objects.all()
    serializer_class = PlotSerializer


# @method_decorator(csrf_exempt, name="dispatch")
# class CultureViewSet(viewsets.ModelViewSet):
#     queryset = Culture.objects.all()
#     serializer_class = CultureSerializer

@method_decorator(csrf_exempt, name="dispatch")
class UserPlotView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        plot = Plot.objects.filter(user=user_id)
        serializer = PlotSerializer(plot, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name="dispatch")
class CultureFieldView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        culture = CultureField.objects.filter(plot__user=user_id)
        serializer = CultureFieldSerializerInline(culture, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CultureFieldSerializerInlinePost(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer


class CurrentUserCropsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """required user id. return all crops belong to current user"""
        user_id = kwargs["user_id"]
        crops = Crop.objects.filter(culture__plot__user=user_id)
        serializer = CropSerializer(crops, many=True)
        return Response(serializer.data, status=200)
