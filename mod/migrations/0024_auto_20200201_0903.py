# Generated by Django 2.2 on 2020-02-01 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0023_mod_modnsfw'),
    ]

    operations = [
        migrations.AddField(
            model_name='modedit',
            name='modNSFW',
            field=models.BooleanField(default=False, verbose_name='NSFW?'),
        ),
        migrations.AlterField(
            model_name='mod',
            name='modNSFW',
            field=models.BooleanField(default=False, verbose_name='NSFW?'),
        ),
    ]
