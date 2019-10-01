from django.contrib import admin
from django.db import models
from django.forms import Textarea

# Register your models here.

from .models import AdminNews


class AdminNewsAdmin(admin.ModelAdmin):
    list_display = ['adminNewsID', 'adminNewsUserID', 'adminNewsText', 'adminNewsDate']
    formfield_overrides = {
        models.CharField: {'widget': Textarea()}
    }


admin.site.register(AdminNews, AdminNewsAdmin)
