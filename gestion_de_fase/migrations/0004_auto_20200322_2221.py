# Generated by Django 3.0.4 on 2020-03-22 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_fase', '0003_auto_20200321_2251'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fase',
            options={'permissions': [('pp_crear_fase', 'Crear Fase dentro de Proyecto'), ('pp_f_eliminar_fase', 'Eliminar Fase de Proyecto'), ('pp_f_cerrar_fase', 'Cerrar Fase de Proyecto')]},
        ),
    ]
