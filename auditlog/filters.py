from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

class ResourceTypeFilter(SimpleListFilter):
    # Filter title displayed in the admin interface
    title = _("Tables")
    
    # Parameter name used in the URL query
    parameter_name = "resource_type"

    def lookups(self, request, model_admin):
        # Get the queryset from the model admin
        qs = model_admin.get_queryset(request)
        
        # Initialize an empty list to store lookups
        query = []
        
        # Iterate through the queryset
        for i in qs:
            # Retrieve the name of the content type based on the content_type_id
            name = ContentType.objects.get(pk=i.content_type_id).name
            
            # Append a tuple (content_type_id, name) to the query list
            query.append((i.content_type_id, name))
        
        # Return a set of unique lookups
        return set(query)

    def queryset(self, request, queryset):
        # Check if a value is selected in the filter
        if self.value() is None:
            return queryset
        
        # Filter the queryset based on the selected resource type (content_type_id)
        return queryset.filter(content_type_id=self.value())

class CIDFilter(SimpleListFilter):
    # Filter title displayed in the admin interface
    title = _("Correlation ID")
    
    # Parameter name used in the URL query
    parameter_name = "cid"

    def lookups(self, request, model_admin):
        # Return an empty list of lookups since CIDFilter does not have predefined options
        return []

    def has_output(self):
        # Indicate that the filter has an output
        return True

    def queryset(self, request, queryset):
        # Check if a value is selected in the filter
        if self.value() is None:
            return queryset
        
        # Filter the queryset based on the selected correlation ID (cid)
        return queryset.filter(cid=self.value())
