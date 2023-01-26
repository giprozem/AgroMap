# Generated by Django 4.1.2 on 2023-01-26 09:21

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0013_alter_landtype_options_contour_is_rounded_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalregion',
            name='polygon',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, geography='Kyrgyzstan', null=True, srid=4326, verbose_name='Контур'),
        ),
        migrations.AddField(
            model_name='region',
            name='polygon',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, geography='Kyrgyzstan', null=True, srid=4326, verbose_name='Контур'),
        ),
    ]
