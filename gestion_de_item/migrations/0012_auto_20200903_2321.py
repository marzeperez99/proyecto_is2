# Generated by Django 3.0.5 on 2020-09-04 03:21

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_item', '0011_auto_20200823_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atributoitemarchivo',
            name='archivo_temporal',
            field=models.FileField(null=True, upload_to='items'),
        ),
        migrations.AlterField(
            model_name='atributoitemarchivo',
            name='valor',
            field=models.FileField(null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to='items'),
        ),
    ]
