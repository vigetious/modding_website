from django.db import models
from django.contrib.auth.models import AbstractUser, User, BaseUserManager, AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth import get_user_model
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

from easy_thumbnails.fields import ThumbnailerImageField

# Create your models here.

def avatar_path(instance, filename):
    return 'files/user_{0}/avatar/{1}'.format(instance.user.id, filename)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    description = models.CharField(max_length=1000, null=True)

    REQUIRED_FIELDS = ('username', 'password')

    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'accounts'
    pass

    def __str__(self):
        return self.email

    def clean(self):
        try:
            if self.avatar.size > settings.MAX_AVATAR_UPLOAD_SIZE:
                raise ValidationError('Your avatar cannot be larger than 10MB.')
        except ValueError:
            pass



class Avatar(models.Model):
    avatarID = models.AutoField("avatar id", primary_key=True, unique=True)
    avatarUserID = models.ForeignKey('User', on_delete=models.CASCADE, related_name="avatarUser")
    avatarImage = ThumbnailerImageField('avatar image', upload_to=avatar_path, blank=True, resize_source=dict(size=(100, 100), sharpen=True))