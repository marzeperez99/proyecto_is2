# Generated by Django 3.0.4 on 2020-03-31 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_proyecto', '0014_auto_20200331_0002'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proyecto',
            options={'permissions': [('ps_crear_proyecto', 'Crear Proyecto'), ('ps_cancelar_proyecto', 'Cancelar Proyecto'), ('ps_ver_proyecto', 'Visualizar lista de todos los Proyectos guardados en el Sistema'), ('g_pp_iniciar_proyecto', 'Iniciar Proyecto'), ('pp_ver_proyecto', 'Visualizar Proyecto')]},
        ),
    ]