from django.db import models
from django.forms import ModelForm
import os
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.postgres.search import SearchVectorField, SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.conf import settings

from taggit.managers import TaggableManager
import django_filters
from easy_thumbnails.fields import ThumbnailerImageField

# Create your models here.


def mod_directory_path(instance, filename):
    return 'files/user_{0}/mods/{1}/{2}'.format(instance.modAuthor.id, instance.modID, filename)

def mod_image_directory_path(instance, filename):
    return 'files/user_{0}/mods/{1}/images/{2}'.format(instance.modAuthor.id, instance.modID, filename)


class ModManager(models.Manager):
    def with_documents(self):
        vector = SearchVector('modName', weight='A') + \
                 SearchVector('modAuthor', weight='B') + \
                 SearchVector('modDescription', weight='C')
        return self.get_queryset().annotate(document=vector)


    def clean(self):
        if self.avatar.size > settings.MAX_AVATAR_UPLOAD_SIZE:
            raise ValidationError('Your avatar image must not be larger than 10MB.')

class Mod(models.Model):
    statusChoices = (
        ('Full release', 'Full release'),
        ('Demo', 'Demo'),
        ('Concept', 'Concept'),
    )
    tiledStretchedChoices = (
        ('Tiled', 'Tiled'),
        ('Stretched', 'Stretched'),
    )
    modID = models.AutoField("mod id", primary_key=True, unique=True)
    modAuthor = models.ForeignKey('accounts.User', on_delete=models.CASCADE, to_field='id')
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
    modUpload = models.FileField(upload_to=mod_directory_path, blank=True, null=True,
                                 validators=[FileExtensionValidator(allowed_extensions=['zip', 'rar'])])
    modUploadURL = models.URLField("mod upload destination", max_length=1000, blank=True)
    modPlayTimeHours = models.IntegerField('mod average playtime hours', blank=True, null=True, default=0)
    modPlayTimeMinutes = models.IntegerField('mod average playtime minutes', blank=True, null=True, default=0)
    modSearch = SearchVectorField(null=True)
    modRating = models.IntegerField('mod average rating', blank=True, null=True, default=0)
    modBackground = models.ImageField('mod background image', upload_to=mod_image_directory_path, blank=True)
    modBackgroundTiledStretch = models.CharField('mod background tiled or stretch', choices=tiledStretchedChoices,
                                                     default=tiledStretchedChoices[0], max_length=100)
    modAvatar = ThumbnailerImageField('mod avatar image', upload_to=mod_image_directory_path, blank=True, resize_source=dict(size=(100, 100), sharpen=True))


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
        try:
            if self.modUpload.size > settings.MAX_UPLOAD_SIZE:
                raise ValidationError('You cannot upload files larger than 1GB.')
        except ValueError:
            pass
        try:
            if self.modBackground.size > settings.MAX_BACKGROUND_UPLOAD_SIZE:
                raise ValidationError('The background image cannot be larger than 20MB.')
        except ValueError:
            pass
        try:
            if self.modAvatar.size > settings.MAX_AVATAR_UPLOAD_SIZE:
                raise ValidationError('The avatar image cannot be larger than 10MB.')
        except ValueError:
            pass

    def __str__(self):
        return self.modName

    def __int__(self):
        return self.modID


class ReviewRating(models.Model):
    reviewid = models.AutoField("review id", primary_key=True)
    reviewModID = models.ForeignKey(Mod, on_delete=models.CASCADE, related_name="reviewModID", to_field="modID")
    #reviewAuthor = models.CharField("review author name", max_length=100)
    reviewAuthorID = models.ForeignKey('accounts.User', on_delete=models.CASCADE, to_field='id')
    reviewDate = models.DateTimeField("review date", auto_now_add=True)
    reviewComment = models.CharField("review comment", max_length=10000, blank=True)
    reviewVotes = models.IntegerField("total votes for comment", default=0)

    def __int__(self):
        return self.reviewid

    def __unicode__(self):
        return self.reviewid

    def __str__(self):
        return str(self.reviewid)


class Vote(models.Model):
    voteID = models.AutoField("vote ID", primary_key=True)
    voteReviewID = models.ForeignKey(ReviewRating, on_delete=models.CASCADE, to_field="reviewid")
    voteAuthor = models.CharField("vote author name", max_length=100)
    voteValue = models.SmallIntegerField("vote value", default=0)

    class Meta:
        unique_together = ('voteAuthor', 'voteReviewID')

    def __unicode__(self):
        return self.voteID

    def __str__(self):
        return str(self.voteID)

    def __int__(self):
        return self.voteID

    def totalVotes(self, id):
        yaes = Vote.objects.get(VoteReviewID=id)


class Rating(models.Model):
    ratingID = models.AutoField("rating ID", primary_key=True)
    ratingModID = models.ForeignKey(Mod, on_delete=models.CASCADE, to_field="modID")
    ratingAuthorID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="id")
    ratingValue = models.PositiveSmallIntegerField("rating value", default=0)

    class Meta:
        unique_together = ('ratingAuthorID', 'ratingModID')


class News(models.Model):
    newsID = models.AutoField("news ID", primary_key=True)
    newsModID = models.ForeignKey(Mod, on_delete=models.CASCADE, to_field="modID")
    newsDate = models.DateTimeField("news publish date", auto_now=True)
    newsText = models.CharField("news text", max_length=5000)


class NewsNotifications(models.Model):
    newsNotificationsID = models.AutoField("new notifications ID", primary_key=True)
    newsNotificationsModID = models.ForeignKey(Mod, on_delete=models.CASCADE, to_field="modID")
    newsNotificationsUserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="id")

    class Meta:
        unique_together = ('newsNotificationsModID', 'newsNotificationsUserID')
