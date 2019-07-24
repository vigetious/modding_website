from django.db import models
from django.forms import ModelForm
import os
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.postgres.search import SearchVectorField, SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.aggregates import StringAgg

from taggit.managers import TaggableManager
import django_filters

# Create your models here.


def user_directory_path(instance, filename):
    return 'files/user_{0}/{1}'.format(instance.modAuthor.id, filename)


class ModManager(models.Manager):
    def with_documents(self):
        vector = SearchVector('modName', weight='A') + \
                 SearchVector('modAuthor', weight='B') + \
                 SearchVector('modDescription', weight='C')
        return self.get_queryset().annotate(document=vector)


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
    tags = TaggableManager()
    modCreditPerms = models.CharField("mod credits and permissions", max_length=1000, blank=True)
    modDonations = models.CharField("mod donation link", max_length=1000, blank=True)
    modDiscord = models.CharField("mod discord link", max_length=100, blank=True)
    modUpload = models.FileField(upload_to=user_directory_path, blank=True, null=True,
                                 validators=[FileExtensionValidator(allowed_extensions=['zip', 'rar'])])
    modUploadURL = models.URLField("mod upload destination", max_length=1000, blank=True)
    modPlayTimeHours = models.IntegerField('mod average playtime hours', blank=True, null=True, default=0)
    modPlayTimeMinutes = models.IntegerField('mod average playtime minutes', blank=True, null=True, default=0)
    modSearch = SearchVectorField(null=True)

    objects = ModManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if 'update_fields' not in kwargs or 'modSearch' not in kwargs['update_fields']:
            instance = self._meta.default_manager.with_documents().get(pk=self.pk)
            instance.modSearch = instance.document
            instance.save(update_fields=['modSearch'])

    class Meta:
        indexes = [
            GinIndex(fields=['modSearch'])
        ]

    def clean(self):
        if self.modPlayTimeMinutes >= 59:
            raise ValidationError('Minutes must be lower than 60.')

    def __str__(self):
        return self.modName


#class ModFilter(django_filters.FilterSet):
#    class Meta:
#        model = Mod
#        fields = [Mod.modTag.names]
