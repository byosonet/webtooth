# Generated by Django 2.2.3 on 2021-01-07 21:25

import appGestionPacientes.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appGestionPacientes', '0046_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField(blank=True, null=True)),
                ('userCode', models.CharField(blank=True, max_length=100, null=True, verbose_name='Usuario')),
                ('userName', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre de usuario')),
                ('nameRecipe', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre del paciente')),
                ('subjectRecipe', models.CharField(blank=True, max_length=100, null=True, verbose_name='Asunto')),
                ('emailRecipe', models.CharField(blank=True, max_length=100, null=True, verbose_name='Email')),
                ('descRecipe', models.CharField(blank=True, max_length=3999, null=True, verbose_name='Receta')),
                ('stateRecipe', models.CharField(blank=True, max_length=100, null=True, verbose_name='Estado')),
                ('dateSend', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de envío')),
            ],
            options={
                'verbose_name': 'Receta',
                'verbose_name_plural': 'Recetas',
                'permissions': [('listRecipe', 'Listar recetas'), ('addRecipe', 'Agregar receta'), ('deleteRecipe', 'Eliminar receta')],
            },
            bases=(appGestionPacientes.mixins.AuditModel, models.Model),
        ),
    ]
