from django.db import models
from django.forms import ModelForm
import os
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.postgres.search import SearchVectorField, SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.conf import settings

#from taggit.managers import TaggableManager
from taggit_selectize.managers import TaggableManager
import django_filters
from easy_thumbnails.fields import ThumbnailerImageField
from embed_video.fields import EmbedVideoField

import random, string

# Create your models here.


def randomStringDigits():
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(50))


def mod_directory_path(instance, filename):
    return 'files/user_{0}/mods/{1}/{2}'.format(instance.modAuthor.id, instance.modID, randomStringDigits())


def mod_image_directory_path(instance, filename):
    return 'files/user_{0}/mods/{1}/images/{2}'.format(instance.modAuthor.id, instance.modID, randomStringDigits())


def mod_preview_image_directory_path(instance, filename):
    return 'files/user_{0}/mods/{1}/images/previews/{2}'.format(instance.modAuthor.id, instance.modID, randomStringDigits())


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
    )
    tiledStretchedChoices = (
        ('Tiled', 'Tiled'),
        ('Stretched', 'Stretched'),
    )
    modID = models.AutoField("mod id", primary_key=True, unique=True)
    modAuthor = models.ForeignKey('accounts.User', on_delete=models.CASCADE, to_field='id')
    modDate = models.DateTimeField("mod publish date", null=True)
    modUpdate = models.DateTimeField("mod most recent update date")
    modStatus = models.CharField(choices=statusChoices, default=statusChoices[0], max_length=100)
    modName = models.CharField("Mod Name", max_length=100)
    modDescription = models.CharField("Mod Description", max_length=10000,
                                      help_text="You can format the description using HTML tags, such as h1, b, and lists.")
    modShortDescription = models.CharField("Mod Short Description", max_length=250,
                                           help_text="This should be short version of the above. Please keep it down to"
                                                     " a few short sentences.", blank=True)
    modWebsite = models.CharField("Mod Website", max_length=100, blank=True)
    tags = TaggableManager()
    modUpload = models.FileField(upload_to=mod_directory_path, blank=True, null=True,
                                 validators=[FileExtensionValidator(allowed_extensions=['zip', 'rar'])])
    modUploadURL = models.URLField("Mod Upload Destination", max_length=1000, help_text="Only Google Drive and MEGA are currently supported.")
    modPlayTimeHours = models.IntegerField('Average Play Time Hours', blank=True, null=True, default=0,
                                           validators=[MinValueValidator(0)])
    modPlayTimeMinutes = models.IntegerField('Average Play Time Minutes', blank=True, null=True, default=0,
                                             validators=[MaxValueValidator(59), MinValueValidator(0)])
    modSearch = SearchVectorField(null=True)
    modRating = models.FloatField('mod average rating', blank=True, null=True, default=0)
    modPreviewVideo = EmbedVideoField('Trailer Video', help_text="Only YouTube and Vimeo links are currently supported.", blank=True)
    modPreviewImage1 = models.ImageField('1st Preview Image', upload_to=mod_preview_image_directory_path, blank=True)
    modPreviewImage2 = models.ImageField('2nd Preview Image', upload_to=mod_preview_image_directory_path, blank=True)
    modPreviewImage3 = models.ImageField('3rd Preview Image', upload_to=mod_preview_image_directory_path, blank=True)
    modPreviewImage4 = models.ImageField('4th Preview Image', upload_to=mod_preview_image_directory_path, blank=True)
    modPreviewImage5 = models.ImageField('5th Preview Image', upload_to=mod_preview_image_directory_path, blank=True)
    modBackground = models.ImageField('Background Image', upload_to=mod_image_directory_path, blank=True)
    modBackgroundTiledStretch = models.CharField('mod background tiled or stretch', choices=tiledStretchedChoices,
                                                     default=tiledStretchedChoices[0], max_length=100,
                                                 help_text="What is tiled and/or stretched?")
    modAvatar = ThumbnailerImageField('Avatar Image', upload_to=mod_image_directory_path, blank=True,
                                      resize_source=dict(size=(200, 200), sharpen=True, upscale=True),
                                      help_text="Recommended size is 200x200. Make sure the background is transparent,"
                                                " as well.")
    modApproved = models.BooleanField('mod moderation approval', default=False)
    modIP = models.CharField('mod user ip address', max_length=100)


    objects = ModManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if 'update_fields' not in kwargs or 'modSearch' not in kwargs['update_fields']:
            instance = self._meta.default_manager.with_documents().get(pk=self.pk)
            instance.modSearch = instance.document
            instance.save(update_fields=['modSearch'])

    def getReviewCount(self):
        return ReviewRating.objects.filter(reviewModID=self.modID).count()

    modReviewCount = property(getReviewCount)

    class Meta:
        indexes = [
            GinIndex(fields=['modSearch'])
        ]
        get_latest_by = "modDate"

    def clean(self):
        if self.modPlayTimeMinutes > 59:
            raise ValidationError('Minutes must be lower than 60.')
        try:
            if self.modPlayTimeMinutes < 0:
                raise ValidationError('Minutes cannot be lower than 0.')
        except ValueError:
            pass
        try:
            if self.modPlayTimeHours < 0:
                raise ValidationError('Hours cannot be lower than 0.')
        except ValueError:
            pass
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
        try:
            if len(self.modShortDescription) > 250:
                raise ValidationError('The short description must be less than 250 letters.')
        except ValueError:
            pass
        try:
            if self.tags == '':
                raise ValidationError('You must have at least one tag.')
        except ValueError:
            pass

    def __str__(self):
        return self.modName

    def __int__(self):
        return self.modID

    def get_latest_by(self):
        return self.modDate


class ReviewRating(models.Model):
    reviewid = models.AutoField("review id", primary_key=True)
    reviewModID = models.ForeignKey(Mod, on_delete=models.CASCADE, related_name="reviewModID", to_field="modID")
    reviewAuthorID = models.ForeignKey('accounts.User', on_delete=models.CASCADE, to_field='id')
    reviewDate = models.DateTimeField("review date", auto_now_add=True)
    reviewComment = models.CharField("review comment", max_length=10000, blank=True)
    reviewVotes = models.IntegerField("total votes for comment", default=0)
    reviewApproved = models.BooleanField('review moderation approval', default=False)

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
    statusChoices = (
        ('Played', 'Played'),
        ('Want to play', 'Want to play'),
    )
    ratingID = models.AutoField("rating ID", primary_key=True)
    ratingModID = models.ForeignKey(Mod, on_delete=models.CASCADE, to_field="modID")
    ratingAuthorID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="id")
    ratingChoice = models.CharField('rating choice', choices=statusChoices,
                                    default=statusChoices[0], max_length=100)
    ratingValue = models.PositiveSmallIntegerField("rating value", null=True)
    ratingNote = models.CharField('rating note', max_length=1000, default="")

    def getAvatar(self):
        if Mod.objects.get(modID=self.ratingModID).modAvatar.url != None:
            return Mod.objects.get(modID=self.ratingModID).modAvatar.url
        else:
            return 'files/'

    def getStatus(self):
        return Mod.objects.get(modID=self.ratingModID).modStatus

    ratingAvatar = property(getAvatar)
    ratingStatus = property(getStatus)

    class Meta:
        unique_together = ('ratingAuthorID', 'ratingModID')


class News(models.Model):
    newsID = models.AutoField("news ID", primary_key=True)
    newsModID = models.ForeignKey(Mod, on_delete=models.CASCADE, to_field="modID")
    newsDate = models.DateTimeField("news publish date", auto_now=True)
    newsText = models.CharField("news text", max_length=5000)
    newsIP = models.CharField("news user ip", max_length=100)


class NewsNotifications(models.Model):
    newsNotificationsID = models.AutoField("new notifications ID", primary_key=True)
    newsNotificationsModID = models.ForeignKey(Mod, on_delete=models.CASCADE, to_field="modID")
    newsNotificationsUserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="id")

    class Meta:
        unique_together = ('newsNotificationsModID', 'newsNotificationsUserID')
