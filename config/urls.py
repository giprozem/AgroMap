from agrobase.views import MaterialViewSet, MaterialBlockViewSet, MaterialImageViewSet
from config import settings
from plot.views import PlotViewSet, UserPlotView, CultureFieldView, CropViewSet, CurrentUserCropsAPIView
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
router.register('agro_base/material', MaterialViewSet)
router.register('agro_base/block', MaterialBlockViewSet)
router.register('agro_base/image', MaterialImageViewSet)

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

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
