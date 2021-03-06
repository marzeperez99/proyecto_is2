# Generated by Django 3.0.4 on 2020-03-22 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_fase', '0004_auto_20200322_2221'),
        ('auth', '0011_update_proxy_permissions'),
        ('roles_de_proyecto', '0005_auto_20200321_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermisosPorFase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_de_fase.Fase')),
                ('permisos', models.ManyToManyField(to='auth.Permission')),
            ],
        ),
    ]
