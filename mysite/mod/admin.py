from django.contrib import admin

from .models import Mod

# Register your models here.

class ModAdmin(admin.ModelAdmin):
    list_display = ['modID', 'modAuthor', 'modDate', 'modUpdate', 'modDownloads', 'modStatus', 'modName',
                    'modDescription', 'modWebsite', 'modTag', 'modCreditPerms', 'modDonations', 'modDiscord',
                    'modUpload']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('modTag')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


admin.site.register(Mod, ModAdmin)
