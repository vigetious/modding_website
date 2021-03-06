# Generated by Django 2.2.2 on 2019-11-25 17:58

from django.conf import settings
import django.contrib.postgres.indexes
import django.contrib.postgres.search
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import embed_video.fields
import mod.models
import taggit_selectize.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('mod', '0008_vote'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModEdit',
            fields=[
                ('modID', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='mod id')),
                ('modDate', models.DateTimeField(null=True, verbose_name='mod publish date')),
                ('modUpdate', models.DateTimeField(verbose_name='mod most recent update date')),
                ('modStatus', models.CharField(choices=[('Full release', 'Full release'), ('Demo', 'Demo')], default=('Full release', 'Full release'), max_length=100)),
                ('modName', models.CharField(max_length=100, verbose_name='Mod Name')),
                ('modDescription', models.CharField(help_text='You can format the description using HTML tags, such as h1, b, and lists.', max_length=10000, verbose_name='Mod Description')),
                ('modShortDescription', models.CharField(blank=True, help_text='This should be short version of the above. Please keep it down to a few short sentences.', max_length=250, verbose_name='Mod Short Description')),
                ('modWebsite', models.CharField(blank=True, max_length=100, verbose_name='Mod Website')),
                ('modUpload', models.FileField(blank=True, null=True, upload_to=mod.models.mod_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['zip', 'rar'])])),
                ('modUploadURL', models.URLField(help_text='Only Google Drive and MEGA are currently supported.', max_length=1000, verbose_name='Mod Upload Destination')),
                ('modPlayTimeHours', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Average Play Time Hours')),
                ('modPlayTimeMinutes', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(59), django.core.validators.MinValueValidator(0)], verbose_name='Average Play Time Minutes')),
                ('modSearch', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('modRating', models.FloatField(blank=True, default=0, null=True, verbose_name='mod average rating')),
                ('modPreviewVideo', embed_video.fields.EmbedVideoField(blank=True, help_text='Only YouTube and Vimeo links are currently supported.', verbose_name='Trailer Video')),
                ('modPreviewImage1', models.ImageField(blank=True, upload_to=mod.models.mod_preview_image_directory_path, verbose_name='1st Preview Image')),
                ('modPreviewImage2', models.ImageField(blank=True, upload_to=mod.models.mod_preview_image_directory_path, verbose_name='2nd Preview Image')),
                ('modPreviewImage3', models.ImageField(blank=True, upload_to=mod.models.mod_preview_image_directory_path, verbose_name='3rd Preview Image')),
                ('modPreviewImage4', models.ImageField(blank=True, upload_to=mod.models.mod_preview_image_directory_path, verbose_name='4th Preview Image')),
                ('modPreviewImage5', models.ImageField(blank=True, upload_to=mod.models.mod_preview_image_directory_path, verbose_name='5th Preview Image')),
                ('modBackground', models.ImageField(blank=True, upload_to=mod.models.mod_image_directory_path, verbose_name='Background Image')),
                ('modBackgroundTiledStretch', models.CharField(choices=[('Tiled', 'Tiled'), ('Stretched', 'Stretched')], default=('Tiled', 'Tiled'), help_text='What is tiled and/or stretched?', max_length=100, verbose_name='mod background tiled or stretch')),
                ('modAvatar', easy_thumbnails.fields.ThumbnailerImageField(blank=True, help_text='Recommended size is 200x200. Make sure the background is transparent, as well.', upload_to=mod.models.mod_image_directory_path, verbose_name='Avatar Image')),
                ('modApproved', models.BooleanField(default=False, verbose_name='mod moderation approval')),
                ('modIP', models.CharField(max_length=100, verbose_name='mod user ip address')),
                ('modAuthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', taggit_selectize.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'get_latest_by': 'modDate',
            },
        ),
        migrations.AddIndex(
            model_name='modedit',
            index=django.contrib.postgres.indexes.GinIndex(fields=['modSearch'], name='mod_modedit_modSear_9b6962_gin'),
        ),
    ]
