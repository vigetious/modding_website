# Generated by Django 2.2 on 2020-01-30 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0022_remove_modedit_modapproved'),
    ]

    operations = [
        migrations.AddField(
            model_name='mod',
            name='modNSFW',
            field=models.BooleanField(default=False, verbose_name='Is mod nsfw'),
        ),
    ]