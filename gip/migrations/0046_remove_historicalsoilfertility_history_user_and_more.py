# Generated by Django 4.1.2 on 2023-03-22 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0045_alter_contour_ink_alter_historicalcontour_ink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsoilfertility',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalsoilfertility',
            name='soil_productivity',
        ),
        migrations.DeleteModel(
            name='HistoricalSoilClassMap',
        ),
        migrations.DeleteModel(
            name='HistoricalSoilFertility',
        ),
    ]
