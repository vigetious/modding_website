from django.db import models
from django.forms import ModelForm

from taggit.managers import TaggableManager

# Create your models here.


class Mod(models.Model):
    statusChoices = (
        ('Full release', 'Full release'),
        ('Demo', 'Demo'),
        ('Concept', 'Concept'),
    )
    modID = models.AutoField("mod id", primary_key=True)
    modAuthor = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    modDate = models.DateTimeField("mod publish date", null=True)
    modUpdate = models.DateTimeField("mod most recent update date")
    modDownloads = models.IntegerField('', null=True, blank=True)
    modStatus = models.CharField(choices=statusChoices, default=statusChoices[0], max_length=100)
    modName = models.CharField("mod name", max_length=100)
    modDescription = models.CharField("mod description", max_length=10000)
    modWebsite = models.CharField("mod website", max_length=100, blank=True)
    modTag = models.CharField("mod tags", max_length=1000)
    modCreditPerms = models.CharField("mod credits and permissions", max_length=1000, blank=True)
    modDonations = models.CharField("mod donation link", max_length=1000, blank=True)
    modDiscord = models.CharField("mod discord link", max_length=100, blank=True)

    def __str__(self):
        return self.modName
