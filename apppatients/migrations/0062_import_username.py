# Generated by Django 2.2.3 on 2021-03-04 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0061_remove_file_usercode'),
    ]

    operations = [
        migrations.AddField(
            model_name='import',
            name='userName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]