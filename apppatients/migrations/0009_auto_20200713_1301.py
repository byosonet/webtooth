# Generated by Django 2.2.3 on 2020-07-13 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apppatients', '0008_auto_20200713_1232'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patient',
            options={'permissions': [('deletePatient', 'Eliminar paciente'), ('updatePatient', 'Actualizar paciente')], 'verbose_name': 'paciente', 'verbose_name_plural': 'Pacientes'},
        ),
    ]