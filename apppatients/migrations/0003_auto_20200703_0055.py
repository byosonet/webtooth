# Generated by Django 2.2.3 on 2020-07-03 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0002_auto_20200702_1537'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='direction',
            options={'verbose_name': 'dirección', 'verbose_name_plural': 'Direcciones'},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'verbose_name': 'paciente', 'verbose_name_plural': 'Pacientes'},
        ),
    ]
