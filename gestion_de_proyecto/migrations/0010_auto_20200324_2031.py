# Generated by Django 3.0.4 on 2020-03-24 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_proyecto', '0009_auto_20200324_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='descripcion',
            field=models.CharField(max_length=401),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='nombre',
            field=models.CharField(max_length=101),
        ),
    ]
