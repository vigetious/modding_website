from rest_framework import serializers
from taggit_selectize import managers
import django_filters

from mod.models import Mod


class ModSerializer(serializers.ModelSerializer):
    modUpload = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):
        if obj.modUpload:
            return obj.modUpload.url
        else:
            return None

    class Meta:
        model = Mod
        fields = ['modID', 'modAuthor', 'modDate', 'modUpdate', 'modStatus', 'modName', 'modDescription',
                  'modShortDescription', 'modWebsite', 'modUploadURL', 'modPlayTimeHours', 'modPlayTimeMinutes',
                  'modRating', 'modAvatar', 'modShow', 'modEdited', 'modNSFW', 'modUpload']


class ModDownloadSerializer(serializers.ModelSerializer):
    modUpload = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):
        return obj.modUpload.url

    class Meta:
        model = Mod
        fields = ['modUpload']
