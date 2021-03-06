# Generated by Django 2.2.2 on 2019-09-26 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0007_auto_20190926_0828'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('voteID', models.AutoField(primary_key=True, serialize=False, verbose_name='vote ID')),
                ('voteAuthor', models.CharField(max_length=100, verbose_name='vote author name')),
                ('voteValue', models.SmallIntegerField(default=0, verbose_name='vote value')),
                ('voteReviewID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mod.ReviewRating')),
            ],
            options={
                'unique_together': {('voteAuthor', 'voteReviewID')},
            },
        ),
    ]
