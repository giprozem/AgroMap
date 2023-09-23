from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

class ResourceTypeFilter(SimpleListFilter):
    title = _("Tables")
    parameter_name = "resource_type"

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        query = []
        for i in qs:
            name = ContentType.objects.get(pk=i.content_type_id).name
            query.append((i.content_type_id, name))
        return set(query)

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(content_type_id=self.value())

class CIDFilter(SimpleListFilter):
    title = _("Correlation ID")
    parameter_name = "cid"

    def lookups(self, request, model_admin):
        return []

    def has_output(self):
        return True

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(cid=self.value())
