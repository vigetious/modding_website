# Generated by Django 2.2.10 on 2020-05-05 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0031_auto_20200318_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='mod',
            name='modRedditAccount',
            field=models.CharField(blank=True, max_length=100, verbose_name='mod reddit account'),
        ),
    ]
