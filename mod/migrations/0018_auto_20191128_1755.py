# Generated by Django 2.2.2 on 2019-11-28 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0017_remove_modedit_modapproved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modedit',
            name='modID',
            field=models.IntegerField(default=None, verbose_name='mod id'),
        ),
    ]
