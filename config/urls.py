from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from schema_graph.views import Schema
from config import settings

# Create an OpenAPI schema view
schema_view = get_schema_view(
    openapi.Info(
        title='API Agromap',
        default_version='v1',
    ),
    public=True,
)

# Define the URL patterns for the application
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path('hub/', include("hub.urls")),
    path('veg/', include('indexes.urls')),
    path('gip/', include('gip.urls')),
    path('docs/', schema_view.with_ui()),
    path("schema/", Schema.as_view()),
    path('info/', include('culture_model.urls')),
    path('ai/', include('ai.urls')),
    path('account/', include('account.urls')),
]

# Add i18n_patterns for internationalization
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
)

# Serve media and static files during development (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize the admin site header and index title
admin.site.site_header = 'AgroMap'
admin.site.index_title = _("Giprozem reference database")
