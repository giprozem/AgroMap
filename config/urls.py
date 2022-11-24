from schema_graph.views import Schema
from config import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from gip.views.contour import ContourViewSet, PointAPIView

router = DefaultRouter()
router.register('contour', ContourViewSet)

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
    path("schema/", Schema.as_view()),
    path("get_contour", PointAPIView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
