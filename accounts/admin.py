from django.contrib import admin

from .models import Tenant, User


admin.site.register(Tenant)
admin.site.register(User)
