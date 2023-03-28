from django.contrib import admin
from ai.models.productivity import ProductivityML


@admin.register(ProductivityML)
class ProductivityMLAdmin(admin.ModelAdmin):
    pass
