# Generated by Django 3.0.5 on 2020-09-23 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_notificaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='titulo',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notificacion',
            name='mensaje',
            field=models.CharField(max_length=800),
        ),
    ]