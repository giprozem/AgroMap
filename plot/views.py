from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from django.contrib.auth.models import User

from plot.models import Plot, Field, Crop, SoilAnalysis, Fertilizer
from plot.serializers import PlotSerializer, FieldSerializerInline, FieldSerializerInlinePost, \
    CropSerializer, SoilAnalysisSerializer, FertilizerSerializer


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
        culture = Field.objects.filter(owner=user_id)
        serializer = FieldSerializerInline(culture, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = FieldSerializerInlinePost(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer


class CurrentUserCropsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        crops = Crop.objects.filter(culture__owner=user_id)
        serializer = CropSerializer(crops, many=True)
        return Response(serializer.data, status=200)


class SoilAnalysisViewSet(viewsets.ModelViewSet):
    queryset = SoilAnalysis.objects.all()
    serializer_class = SoilAnalysisSerializer


class CurrentUserFertilizerViewSet(viewsets.ModelViewSet):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer
