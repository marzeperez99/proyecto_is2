# Generated by Django 3.0.4 on 2020-03-22 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles_de_proyecto', '0006_permisosporfase'),
        ('gestion_de_proyecto', '0004_auto_20200322_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='participante',
            name='permisos_por_fase',
            field=models.ManyToManyField(to='roles_de_proyecto.PermisosPorFase'),
        ),
        migrations.AlterField(
            model_name='participante',
            name='rol',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='roles_de_proyecto.RolDeProyecto'),
        ),
    ]
