# Generated by Django 2.2.3 on 2020-07-14 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0014_auto_20200713_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='activo',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Activo'),
        ),
    ]
