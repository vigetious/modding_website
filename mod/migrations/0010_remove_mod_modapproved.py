# Generated by Django 2.2.2 on 2019-11-25 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0009_auto_20191125_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mod',
            name='modApproved',
        ),
    ]
