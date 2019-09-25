from django.contrib import admin

# Register your models here.

from .models import AdminNews


class AdminNewsAdmin(admin.ModelAdmin):
    list_display = ['adminNewsID', 'adminNewsUserID', 'adminNewsText', 'adminNewsDate']


admin.site.register(AdminNews, AdminNewsAdmin)
