# Generated by Django 5.0 on 2025-01-27 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='propiedad',
            name='area',
            field=models.CharField(blank=True, default=True, max_length=255),
        ),
        migrations.AddField(
            model_name='propiedad',
            name='numero_registro',
            field=models.CharField(blank=True, default=True, max_length=255),
        ),
        migrations.AddField(
            model_name='propiedad',
            name='ubicacion',
            field=models.CharField(blank=True, default=True, max_length=255),
        ),
    ]
