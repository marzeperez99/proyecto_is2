# Generated by Django 3.0.4 on 2020-03-24 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_fase', '0005_auto_20200324_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='fase',
            name='descripcion',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fase',
            name='fase_anterior',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_de_fase.Fase'),
        ),
    ]
