# Generated by Django 3.0.5 on 2020-08-31 02:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_linea_base', '0002_lineabase_fase'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineabase',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
