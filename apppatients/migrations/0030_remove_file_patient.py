# Generated by Django 2.2.3 on 2020-07-21 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0029_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='patient',
        ),
    ]