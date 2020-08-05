# Generated by Django 2.2.3 on 2020-07-02 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(max_length=50, verbose_name='Calle')),
                ('numeroExt', models.CharField(max_length=50, verbose_name='Número exterior')),
                ('numeroInt', models.CharField(max_length=50, verbose_name='Número interior')),
                ('ciudad', models.CharField(max_length=50, verbose_name='Ciudad')),
                ('estado', models.CharField(max_length=50, verbose_name='Estado')),
                ('cp', models.CharField(max_length=6, verbose_name='Código Postal')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellidoPaterno', models.CharField(max_length=50, verbose_name='Apellido paterno')),
                ('apellidoMaterno', models.CharField(max_length=50, verbose_name='Apellido materno')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo electrónico')),
                ('telefono', models.CharField(max_length=10, verbose_name='Teléfono')),
                ('numexp', models.CharField(max_length=20, verbose_name='Número de expediente')),
                ('fechaAlta', models.DateField(verbose_name='Fecha alta')),
                ('activo', models.BooleanField(verbose_name='Activo')),
            ],
        ),
    ]
