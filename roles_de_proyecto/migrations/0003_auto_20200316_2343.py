# Generated by Django 3.0.4 on 2020-03-16 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles_de_proyecto', '0002_auto_20200316_2017'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='roldeproyecto',
            options={'permissions': (('pp_agregar_item', 'Agregar Item'),)},
        ),
    ]
