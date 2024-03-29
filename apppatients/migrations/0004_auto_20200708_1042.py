# Generated by Django 2.2.3 on 2020-07-08 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0003_auto_20200703_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='activo',
            field=models.BooleanField(blank=True, null=True, verbose_name='Activo'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='fechaAlta',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha alta'),
        ),
    ]
