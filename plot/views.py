from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from plot.models import Plot, Culture
from plot.serializers import PlotSerializer, CultureSerializerInline, PlotCultureSerializer, CultureSerializerInlinePost


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
class CultureView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        plot_id = kwargs["plot_id"]
        culture = Culture.objects.filter(plot__user=user_id, plot=plot_id)
        serializer = CultureSerializerInline(culture, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CultureSerializerInlinePost(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


