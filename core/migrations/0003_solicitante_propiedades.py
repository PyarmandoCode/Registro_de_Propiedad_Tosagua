# Generated by Django 5.0 on 2025-01-31 21:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_propiedad_area_propiedad_numero_registro_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('cedula', models.CharField(max_length=10)),
                ('tipo_solicitud', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Propiedades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bien_inmueble', models.CharField(max_length=255)),
                ('fecha_inscripcion', models.DateField()),
                ('Numero_Inscripcion', models.IntegerField()),
                ('oficina_guarda_original', models.CharField(max_length=255)),
                ('nombre_canton', models.CharField(max_length=255)),
                ('observaciones', models.TextField()),
                ('fecha_resolucion', models.DateField()),
                ('ubicacion', models.CharField(blank=True, default=True, max_length=255)),
                ('area', models.CharField(blank=True, default=True, max_length=255)),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.solicitante')),
            ],
        ),
    ]
