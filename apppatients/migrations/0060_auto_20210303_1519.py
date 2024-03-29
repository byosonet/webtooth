# Generated by Django 2.2.3 on 2021-03-03 21:19

import appfiles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0059_import_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='userCode',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='path',
            field=models.FileField(blank=True, null=True, upload_to=appfiles.models.user_directory_path, verbose_name='Archivo'),
        ),
    ]
