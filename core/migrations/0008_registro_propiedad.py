# Generated by Django 5.0 on 2025-02-01 04:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_propiedades_codigo_interno'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='propiedad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.propiedades'),
        ),
    ]
