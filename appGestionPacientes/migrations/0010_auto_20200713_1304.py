# Generated by Django 2.2.3 on 2020-07-13 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appGestionPacientes', '0009_auto_20200713_1301'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patient',
            options={'permissions': [('addPatient', 'Agregar paciente'), ('viewPatient', 'Ver paciente'), ('deletePatient', 'Eliminar paciente'), ('updatePatient', 'Actualizar paciente')], 'verbose_name': 'paciente', 'verbose_name_plural': 'Pacientes'},
        ),
    ]
