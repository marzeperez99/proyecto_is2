# Generated by Django 3.0.4 on 2020-03-23 02:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_tipo_de_item', '0002_auto_20200321_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atributobinario',
            name='max_tamaño',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'El tamaño maximo para el archivo debe ser mayor o igual a 1MB')]),
        ),
    ]
