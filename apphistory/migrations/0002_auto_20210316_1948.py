# Generated by Django 2.2.3 on 2021-03-17 01:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apphistory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='userId',
        ),
        migrations.RemoveField(
            model_name='group',
            name='userName',
        ),
        migrations.AddField(
            model_name='group',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='group',
            name='fechaAlta',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Fecha alta'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='fechaUpdate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Fecha actualización'),
            preserve_default=False,
        ),
    ]
