# Generated by Django 2.2.3 on 2020-07-27 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0040_auto_20200725_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Propertie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True, verbose_name='key')),
                ('value', models.CharField(blank=True, max_length=100, null=True, verbose_name='value')),
            ],
            options={
                'verbose_name': 'propiedad',
                'verbose_name_plural': 'Propiedades',
            },
        ),
    ]