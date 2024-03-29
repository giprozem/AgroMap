# Generated by Django 4.1.2 on 2023-06-19 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0054_rename_id_historicalsoilclass_id_soil_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Fertility',
        ),
        migrations.RemoveField(
            model_name='historicalfertility',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicallanduse',
            name='contour',
        ),
        migrations.RemoveField(
            model_name='historicallanduse',
            name='culture',
        ),
        migrations.RemoveField(
            model_name='historicallanduse',
            name='farmer',
        ),
        migrations.RemoveField(
            model_name='historicallanduse',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicallandusephotos',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicallandusephotos',
            name='land_use',
        ),
        migrations.RemoveField(
            model_name='historicalorthophoto',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalvillage',
            name='conton',
        ),
        migrations.RemoveField(
            model_name='historicalvillage',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='landuse',
            name='contour',
        ),
        migrations.RemoveField(
            model_name='landuse',
            name='culture',
        ),
        migrations.RemoveField(
            model_name='landuse',
            name='farmer',
        ),
        migrations.RemoveField(
            model_name='landusephotos',
            name='land_use',
        ),
        migrations.DeleteModel(
            name='OrthoPhoto',
        ),
        migrations.RemoveField(
            model_name='soilfertility',
            name='soil_productivity',
        ),
        migrations.RemoveField(
            model_name='village',
            name='conton',
        ),
        migrations.DeleteModel(
            name='HistoricalFertility',
        ),
        migrations.DeleteModel(
            name='HistoricalLandUse',
        ),
        migrations.DeleteModel(
            name='HistoricalLandUsePhotos',
        ),
        migrations.DeleteModel(
            name='HistoricalOrthoPhoto',
        ),
        migrations.DeleteModel(
            name='HistoricalVillage',
        ),
        migrations.DeleteModel(
            name='LandUse',
        ),
        migrations.DeleteModel(
            name='LandUsePhotos',
        ),
        migrations.DeleteModel(
            name='SoilFertility',
        ),
        migrations.DeleteModel(
            name='Village',
        ),
    ]
