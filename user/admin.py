from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (('User Type', {"fields": ["user_type", "shop"]}),)
    list_display = BaseUserAdmin.list_display + ('user_type', 'shop')


admin.site.register(User, UserAdmin)
