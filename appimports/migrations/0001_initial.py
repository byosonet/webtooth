# Generated by Django 2.2.3 on 2021-03-09 19:42

import appimports.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Import',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField(blank=True, null=True)),
                ('userName', models.CharField(blank=True, max_length=100, null=True)),
                ('tipoSubida', models.CharField(max_length=50, verbose_name='Tipo de fichero')),
                ('fechaSubida', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de subida')),
                ('path', models.FileField(blank=True, null=True, upload_to='upload-xls', verbose_name='Archivo')),
                ('importado', models.BooleanField(blank=True, null=True, verbose_name='Importado')),
            ],
            options={
                'verbose_name': 'importado',
                'verbose_name_plural': 'Importados',
                'permissions': [('importFile', 'Subir archivo')],
            },
            bases=(appimports.mixins.AuditModel, models.Model),
        ),
    ]
