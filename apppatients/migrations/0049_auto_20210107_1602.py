# Generated by Django 2.2.3 on 2021-01-07 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0048_propertie_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertie',
            name='key',
            field=models.CharField(max_length=100, verbose_name='key'),
        ),
    ]