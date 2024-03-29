# Generated by Django 2.2.3 on 2021-03-17 02:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import webtooth.mixins


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apphistory', '0007_remove_group_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('fechaAlta', models.DateTimeField(auto_now_add=True, verbose_name='Fecha alta')),
                ('fechaUpdate', models.DateTimeField(auto_now_add=True, verbose_name='Fecha actualización')),
                ('grupo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apphistory.Group', verbose_name='Grupo')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Estudio',
                'verbose_name_plural': 'Estudios',
                'permissions': [('addStudy', 'Agregar estudio'), ('viewStudy', 'Ver estudio'), ('deleteStudy', 'Eliminar estudio'), ('updateStudy', 'Actualizar estudio')],
            },
            bases=(webtooth.mixins.AuditModel, models.Model),
        ),
    ]
