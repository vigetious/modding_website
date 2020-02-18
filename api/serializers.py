from rest_framework import serializers
from taggit_selectize import managers
import django_filters

from mod.models import Mod


class ModSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mod
        fields = ['modID', 'modAuthor', 'modDate', 'modUpdate', 'modStatus', 'modName', 'modDescription',
                  'modShortDescription', 'modWebsite', 'modUploadURL', 'modPlayTimeHours', 'modPlayTimeMinutes',
                  'modRating', 'modAvatar', 'modShow', 'modEdited', 'modNSFW']