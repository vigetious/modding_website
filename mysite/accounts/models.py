from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from easy_thumbnails.fields import ThumbnailerImageField

# Create your models here.

class User(AbstractUser):
    pass
