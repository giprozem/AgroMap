# Generated by Django 4.1.2 on 2023-01-11 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indexes', '0007_alter_historicalindexfact_date_alter_indexfact_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ndviindex',
            name='contour',
        ),
        migrations.DeleteModel(
            name='HistoricalNDVIIndex',
        ),
        migrations.DeleteModel(
            name='NDVIIndex',
        ),
    ]
