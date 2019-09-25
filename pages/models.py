from django.db import models
from django.conf import settings


# Create your models here.

class AdminNews(models.Model):
    adminNewsID = models.AutoField("admin news ID", primary_key=True)
    adminNewsUserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="id")
    adminNewsText = models.CharField("admin news text", max_length=10000)
    adminNewsDate = models.DateTimeField("admin news publish date", auto_now=True)
