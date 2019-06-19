from django.db import models
from django.forms import ModelForm

from taggit.managers import TaggableManager

# Create your models here.


class Mod(models.Model):
    modID = models.AutoField("mod id", primary_key=True)
    modName = models.CharField("mod name", max_length=100)
    modDescription = models.CharField("mod description", max_length=10000)
    modWebsite = models.CharField("mod website", max_length=100, blank=True)
    modTag = models.CharField("mod tags", max_length=1000)
    modCreditPerms = models.CharField("mod credits and permissions", max_length=1000, blank=True)
    modDonations = models.CharField("mod donation link", max_length=1000, blank=True)
    modDiscord = models.CharField("mod discord link", max_length=100, blank=True)

    def __str__(self):
        return self.modName


class ModForm(ModelForm):
    class Meta:
        model = Mod
        fields = ['modName', 'modDescription', 'modWebsite', 'modTag', 'modCreditPerms', 'modDonations', 'modDiscord']
