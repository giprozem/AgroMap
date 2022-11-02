from schema_graph.views import Schema
from config import settings
from plot.views import PlotViewSet, UserPlotView, CultureFieldView, CropViewSet, CurrentUserCropsAPIView, \
    SoilAnalysisViewSet, CurrentUserFertilizerViewSet
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('plots', PlotViewSet)
# router.register('culture', CultureViewSet)
router.register('crop', CropViewSet)
router.register('soil-analysis', SoilAnalysisViewSet)
router.register('fertilizer', CurrentUserFertilizerViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='API PLOT',
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('docs/', schema_view.with_ui()),
    path('plot/<int:user_id>/', UserPlotView.as_view()),
    path('cultures_fields/<int:user_id>/', CultureFieldView.as_view()),
    path('current_user/<int:user_id>/', CurrentUserCropsAPIView.as_view()),
    path("schema/", Schema.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
