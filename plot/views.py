from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets

from plot.models import Plot, Culture
from plot.serializers import PlotSerializer, CultureSerializer


@method_decorator(csrf_exempt, name="dispatch")
class PlotViewSet(viewsets.ModelViewSet):
    queryset = Plot.objects.all()
    serializer_class = PlotSerializer


@method_decorator(csrf_exempt, name="dispatch")
class CultureViewSet(viewsets.ModelViewSet):
    queryset = Culture.objects.all()
    serializer_class = CultureSerializer


