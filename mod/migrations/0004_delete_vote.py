# Generated by Django 2.2.2 on 2019-09-25 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0003_vote'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Vote',
        ),
    ]