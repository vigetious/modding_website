# Generated by Django 2.2.2 on 2019-12-01 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0019_auto_20191128_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='mod',
            name='modEdited',
            field=models.BooleanField(default=False, verbose_name='Has mod got an edit'),
        ),
    ]
