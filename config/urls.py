from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from schema_graph.views import Schema

from account.views.authenticated import LoginAgromapView
from config import settings
from gip.views.geoserver import Geoserver
from hub.views.authetificated import LoginHubView
from hub.views.zem_balance_api import ZemBalanceViewSet

# router = DefaultRouter()
#
# #Zem Balance
# router.register('zem_balance', ZemBalanceViewSet, basename='zem_balance')


schema_view = get_schema_view(
    openapi.Info(
        title='API Agromap and Hub',
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path('hub/', include("hub.urls")),
    path('', include('indexes.urls')),
    path('', include('gip.urls')),
    path('docs/', schema_view.with_ui()),
    path("schema/", Schema.as_view()),
    path('login_agromap/', LoginAgromapView.as_view()),
    path('geoserver/', Geoserver.as_view()),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'AgroMap'
admin.site.index_title = _("Эталонная база данных Гипрозем")
