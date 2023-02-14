from django.contrib import admin

from account.models import MyUser


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    pass