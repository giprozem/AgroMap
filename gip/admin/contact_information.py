from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin

from gip.models import Department, ContactInformation


@admin.register(Department)
class DepartmentAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'name')
    list_filter = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    list_display_links = ('id', 'name')


@admin.register(ContactInformation)
class ContactInformationAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    readonly_fields = ('id', )
    list_display = ('id', 'title', 'fullname')
    list_filter = ('title',)
    ordering = ('title',)
    search_fields = ('title', 'department__name', 'fullname')
    list_display_links = ('id', 'title')

