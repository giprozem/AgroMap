from django.contrib import admin

from agrobase.models import Material, MaterialImage, MaterialBlock


class MaterialImageAdmin(admin.TabularInline):
    model = MaterialImage


class MaterialBlogAdmin(admin.TabularInline):
    model = MaterialBlock


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    inlines = [MaterialBlogAdmin, MaterialImageAdmin]