# Generated by Django 2.2.3 on 2021-03-03 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0060_auto_20210303_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='userCode',
        ),
    ]
