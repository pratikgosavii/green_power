from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_showroom', 'is_distributor']


admin.site.register(User, UserAdmin)
