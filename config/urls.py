from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from config import settings
from plot.views import PlotViewSet, UserPlotView, CultureFieldView

router = DefaultRouter()

# router.register('plot', PlotViewSet)
# router.register('culture', CultureViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('plot/<int:user_id>/', UserPlotView.as_view()),
    path('cultures_fields/<int:user_id>/', CultureFieldView.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
