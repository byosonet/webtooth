# Generated by Django 2.2.3 on 2021-01-07 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0047_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertie',
            name='userId',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
