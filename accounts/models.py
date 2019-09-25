from django.db import models
from django.contrib.auth.models import AbstractUser, User, BaseUserManager, AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth import get_user_model
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

from easy_thumbnails.fields import ThumbnailerImageField
from verified_email_field.forms import VerifiedEmailField

import string, random

# Create your models here.

def randomStringDigits():
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(50))


def avatar_path(instance, filename):
    return 'files/user_{0}/avatar/{1}'.format(instance.avatarUserID.id, randomStringDigits())


class User(AbstractUser):
    email = models.EmailField(unique=True)
    #email = VerifiedEmailField('email', fieldsetup_id='email')
    description = models.CharField(max_length=1000, null=True)
    totalComments = models.IntegerField('total comments', default=0)
    totalMods = models.IntegerField('total mods', default=0)

    REQUIRED_FIELDS = ('username', 'password')

    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'accounts'
    pass

    def __str__(self):
        return self.username


class Avatar(models.Model):
    avatarID = models.AutoField("avatar id", primary_key=True, unique=True)
    avatarUserID = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="avatarUser", to_field="id", unique=True)
    avatarTime = models.DateTimeField(auto_now=True)
    avatarImage = ThumbnailerImageField('avatar image', upload_to=avatar_path, blank=True, resize_source=dict(size=(200, 200), sharpen=True, upscale=True))
    avatarApproved = models.BooleanField('avatar moderation approval', default=False)


    def __str__(self):
        return str(self.avatarUserID)

    def __int__(self):
        return self.avatarID

    def clean(self):
        if self.avatarImage is None:
            raise ValidationError('Please select an image to upload for your avatar, or click back.')
