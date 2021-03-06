# Generated by Django 3.0.6 on 2020-08-24 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_proyecto', '0020_auto_20200401_1759'),
        ('gestion_de_solicitud', '0004_auto_20200823_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignacion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_de_proyecto.Participante'),
        ),
        migrations.AlterField(
            model_name='solicituddecambio',
            name='solicitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_de_proyecto.Participante'),
        ),
        migrations.AlterField(
            model_name='voto',
            name='miembro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_de_proyecto.Participante'),
        ),
    ]
