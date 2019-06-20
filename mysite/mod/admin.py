from django.contrib import admin

from .models import Mod

# Register your models here.

class ModAdmin(admin.ModelAdmin):
    list_display = ['modID', 'modAuthor', 'modDate', 'modUpdate', 'modDownloads', 'modStatus', 'modName',
                    'modDescription', 'modWebsite', 'modTag', 'modCreditPerms', 'modDonations', 'modDiscord']


admin.site.register(Mod, ModAdmin)
