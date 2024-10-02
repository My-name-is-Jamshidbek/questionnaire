from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    ordering = ['username']
    list_display = ['username', 'fullname', 'hemis_token', 'is_staff']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('fullname', 'hemis_token')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'hemis_token', 'fullname', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'hemis_token', 'fullname')
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
