# Generated by Django 2.2.10 on 2020-02-19 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0027_reviewrating_reviewhasedit'),
    ]

    operations = [
        migrations.AddField(
            model_name='modedit',
            name='modBest',
            field=models.BooleanField(default=False, verbose_name='best mod?'),
        ),
        migrations.AddField(
            model_name='modedit',
            name='modRunnerUp',
            field=models.BooleanField(default=False, verbose_name='runner-up mod?'),
        ),
    ]
