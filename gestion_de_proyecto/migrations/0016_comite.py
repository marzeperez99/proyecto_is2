# Generated by Django 3.0.4 on 2020-03-31 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_proyecto', '0015_auto_20200331_0013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miembros', models.ManyToManyField(to='gestion_de_proyecto.Participante')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_de_proyecto.Proyecto')),
            ],
        ),
    ]
