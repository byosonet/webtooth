# Generated by Django 2.2.3 on 2021-01-03 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0044_auto_20210101_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='apellidoMaterno',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Apellido materno'),
        ),
    ]