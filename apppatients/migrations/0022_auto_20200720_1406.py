# Generated by Django 2.2.3 on 2020-07-20 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0021_auto_20200720_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='direccion',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to='apppatients.Address'),
        ),
    ]
