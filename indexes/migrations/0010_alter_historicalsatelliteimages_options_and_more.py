# Generated by Django 4.1.2 on 2023-01-12 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indexes', '0009_historicalsatelliteimages_bbox_satelliteimages_bbox'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalsatelliteimages',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'История', 'verbose_name_plural': 'historical Спутниковые снимки Sentinel -2'},
        ),
        migrations.AlterModelOptions(
            name='satelliteimages',
            options={'verbose_name': 'Спутниковый снимок Sentinel -2', 'verbose_name_plural': 'Спутниковые снимки Sentinel -2'},
        ),
    ]
