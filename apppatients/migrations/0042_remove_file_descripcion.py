# Generated by Django 2.2.3 on 2020-12-15 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0041_propertie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='descripcion',
        ),
    ]