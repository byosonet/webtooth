# Generated by Django 2.2.3 on 2020-07-02 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('marca', models.CharField(max_length=50, verbose_name='Marca')),
                ('cantidad', models.IntegerField(verbose_name='Existencias')),
                ('fechaAlta', models.DateField(max_length=50, verbose_name='Fecha alta')),
                ('fechaBaja', models.DateField(blank=True, null=True, verbose_name='Fecha baja')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
    ]
