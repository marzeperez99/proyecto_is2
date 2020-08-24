# Generated by Django 3.0.5 on 2020-08-23 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestion_linea_base', '0001_initial'),
        ('gestion_de_item', '0010_auto_20200427_2004'),
        ('usuario', '0002_auto_20200317_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudDeCambio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=500)),
                ('fecha', models.DateTimeField()),
                ('numero_de_miembros', models.IntegerField()),
                ('votos_a_favor', models.IntegerField(default=0)),
                ('votos_en_contra', models.IntegerField(default=0)),
                ('linea_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_linea_base.LineaBase')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Voto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voto_a_favor', models.BooleanField()),
                ('miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.Usuario')),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_de_solicitud.SolicitudDeCambio')),
            ],
        ),
        migrations.CreateModel(
            name='Asignacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_de_item.Item')),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_de_solicitud.SolicitudDeCambio')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.Usuario')),
            ],
        ),
    ]
