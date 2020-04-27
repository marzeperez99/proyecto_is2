# Generated by Django 3.0.4 on 2020-03-24 14:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_proyecto', '0005_auto_20200322_2221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='fechaCreacion',
        ),
        migrations.AddField(
            model_name='proyecto',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de Creacion'),
        ),
    ]
