# Generated by Django 3.0.5 on 2020-04-06 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_de_item', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='version',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_version', to='gestion_de_item.VersionItem'),
        ),
    ]
