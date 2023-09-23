# Generated by Django 4.1.2 on 2023-09-23 07:53

import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('culture_model', '0013_alter_classes_options_alter_decade_options_and_more'),
        ('ai', '0015_alter_ai_found_options_alter_contour_ai_options_and_more'),
        ('gip', '0064_alter_contactinformation_options_and_more'),
        ('indexes', '0039_actualvegindex_satellite_image_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actualvegindex',
            options={'verbose_name': 'Actual Index', 'verbose_name_plural': 'Actual Indices'},
        ),
        migrations.AlterModelOptions(
            name='contouraiindexcreatingreport',
            options={'verbose_name': 'Index Creation Report', 'verbose_name_plural': 'Index Creation Reports'},
        ),
        migrations.AlterModelOptions(
            name='contouraverageindex',
            options={'verbose_name': 'Contour Average Index', 'verbose_name_plural': 'Contour Average Indices'},
        ),
        migrations.AlterModelOptions(
            name='historicalactualvegindex',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'History', 'verbose_name_plural': 'historical Actual Indices'},
        ),
        migrations.AlterModelOptions(
            name='historicalcontouraverageindex',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'History', 'verbose_name_plural': 'historical Contour Average Indices'},
        ),
        migrations.AlterModelOptions(
            name='historicalpredictedcontourvegindex',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'History', 'verbose_name_plural': 'historical AI Index Values'},
        ),
        migrations.AlterModelOptions(
            name='historicalproductivityclass',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Productivity Class', 'verbose_name_plural': 'historical Productivity Classes'},
        ),
        migrations.AlterModelOptions(
            name='historicalscihubimagedate',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'History', 'verbose_name_plural': 'historical Sentinel-2 Satellite Images'},
        ),
        migrations.AlterModelOptions(
            name='indexcreatingreport',
            options={'verbose_name': 'Index Report', 'verbose_name_plural': 'Index Reports'},
        ),
        migrations.AlterModelOptions(
            name='indexmeaning',
            options={'verbose_name': 'Index Value', 'verbose_name_plural': 'Index Values'},
        ),
        migrations.AlterModelOptions(
            name='predictedcontourvegindex',
            options={'verbose_name': 'AI Index Value', 'verbose_name_plural': 'AI Index Values'},
        ),
        migrations.AlterModelOptions(
            name='productivityclass',
            options={'verbose_name': 'Productivity Class', 'verbose_name_plural': 'Productivity Classes'},
        ),
        migrations.AlterModelOptions(
            name='satelliteimageband',
            options={'verbose_name': 'Satellite Image Band', 'verbose_name_plural': 'Satellite Image Bands'},
        ),
        migrations.AlterModelOptions(
            name='satelliteimagelayer',
            options={'verbose_name': 'Satellite Image Layer', 'verbose_name_plural': 'Satellite Image Layers'},
        ),
        migrations.AlterModelOptions(
            name='satelliteimagesource',
            options={'verbose_name': 'Satellite Image Source', 'verbose_name_plural': 'Satellite Image Sources'},
        ),
        migrations.AlterModelOptions(
            name='scihubareainterest',
            options={'verbose_name': 'Satellite Image Area of Interest', 'verbose_name_plural': 'Satellite Image Areas of Interest'},
        ),
        migrations.AlterModelOptions(
            name='scihubimagedate',
            options={'verbose_name': 'Sentinel-2 Satellite Image', 'verbose_name_plural': 'Sentinel-2 Satellite Images'},
        ),
        migrations.AlterField(
            model_name='actualvegindex',
            name='average_value',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, verbose_name='Average Index Value'),
        ),
        migrations.AlterField(
            model_name='actualvegindex',
            name='contour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actual_veg_index', to='gip.contour', verbose_name='Field Contours'),
        ),
        migrations.AlterField(
            model_name='actualvegindex',
            name='date',
            field=models.DateField(help_text='Enter the date of the satellite image used to calculate the index', verbose_name='Analysis Date'),
        ),
        migrations.AlterField(
            model_name='actualvegindex',
            name='index',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='culture_model.vegetationindex', verbose_name='Index'),
        ),
        migrations.AlterField(
            model_name='actualvegindex',
            name='index_image',
            field=models.FileField(blank=True, upload_to='index_image', verbose_name='Index Image'),
        ),
        migrations.AlterField(
            model_name='actualvegindex',
            name='meaning_of_average_value',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='indexes.indexmeaning', verbose_name='Meaning of Average Index Value'),
        ),
        migrations.AlterField(
            model_name='contouraiindexcreatingreport',
            name='contour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ai.contour_ai', verbose_name='Contour'),
        ),
        migrations.AlterField(
            model_name='contouraiindexcreatingreport',
            name='is_processed',
            field=models.BooleanField(default=False, verbose_name='Process Initiated'),
        ),
        migrations.AlterField(
            model_name='contouraiindexcreatingreport',
            name='process_error',
            field=models.TextField(verbose_name='Processing Errors'),
        ),
        migrations.AlterField(
            model_name='contouraiindexcreatingreport',
            name='satellite_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='indexes.scihubimagedate', verbose_name='Satellite Image'),
        ),
        migrations.AlterField(
            model_name='contouraiindexcreatingreport',
            name='veg_index',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='culture_model.vegetationindex', verbose_name='Vegetation Index'),
        ),
        migrations.AlterField(
            model_name='contouraverageindex',
            name='contour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gip.contour', verbose_name='Field Contours'),
        ),
        migrations.AlterField(
            model_name='contouraverageindex',
            name='end_day',
            field=models.DateField(verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='contouraverageindex',
            name='index_count',
            field=models.IntegerField(verbose_name='Number of Indices Used for Calculation'),
        ),
        migrations.AlterField(
            model_name='contouraverageindex',
            name='productivity_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indexes.productivityclass', verbose_name='Productivity Class'),
        ),
        migrations.AlterField(
            model_name='contouraverageindex',
            name='start_day',
            field=models.DateField(verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='contouraverageindex',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, verbose_name='Average Index Value'),
        ),
        migrations.AlterField(
            model_name='historicalactualvegindex',
            name='average_value',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, verbose_name='Average Index Value'),
        ),
        migrations.AlterField(
            model_name='historicalactualvegindex',
            name='contour',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.contour', verbose_name='Field Contours'),
        ),
        migrations.AlterField(
            model_name='historicalactualvegindex',
            name='date',
            field=models.DateField(help_text='Enter the date of the satellite image used to calculate the index', verbose_name='Analysis Date'),
        ),
        migrations.AlterField(
            model_name='historicalactualvegindex',
            name='index',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='culture_model.vegetationindex', verbose_name='Index'),
        ),
        migrations.AlterField(
            model_name='historicalactualvegindex',
            name='index_image',
            field=models.TextField(blank=True, max_length=100, verbose_name='Index Image'),
        ),
        migrations.AlterField(
            model_name='historicalactualvegindex',
            name='meaning_of_average_value',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='indexes.indexmeaning', verbose_name='Meaning of Average Index Value'),
        ),
        migrations.AlterField(
            model_name='historicalcontouraverageindex',
            name='contour',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.contour', verbose_name='Field Contours'),
        ),
        migrations.AlterField(
            model_name='historicalcontouraverageindex',
            name='end_day',
            field=models.DateField(verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='historicalcontouraverageindex',
            name='index_count',
            field=models.IntegerField(verbose_name='Number of Indices Used for Calculation'),
        ),
        migrations.AlterField(
            model_name='historicalcontouraverageindex',
            name='productivity_class',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='indexes.productivityclass', verbose_name='Productivity Class'),
        ),
        migrations.AlterField(
            model_name='historicalcontouraverageindex',
            name='start_day',
            field=models.DateField(verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='historicalcontouraverageindex',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, verbose_name='Average Index Value'),
        ),
        migrations.AlterField(
            model_name='historicalpredictedcontourvegindex',
            name='average_value',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, verbose_name='Average Index Value'),
        ),
        migrations.AlterField(
            model_name='historicalpredictedcontourvegindex',
            name='contour',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ai.contour_ai', verbose_name='Contour'),
        ),
        migrations.AlterField(
            model_name='historicalpredictedcontourvegindex',
            name='date',
            field=models.DateField(verbose_name='Analysis Date'),
        ),
        migrations.AlterField(
            model_name='historicalpredictedcontourvegindex',
            name='index',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='culture_model.vegetationindex', verbose_name='Index'),
        ),
        migrations.AlterField(
            model_name='historicalpredictedcontourvegindex',
            name='index_image',
            field=models.TextField(blank=True, max_length=100, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='historicalpredictedcontourvegindex',
            name='meaning_of_average_value',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='indexes.indexmeaning', verbose_name='Index Value'),
        ),
        migrations.AlterField(
            model_name='historicalproductivityclass',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='historicalproductivityclass',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='historicalproductivityclass',
            name='description_ky',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='historicalproductivityclass',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='historicalproductivityclass',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='historicalproductivityclass',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='historicalproductivityclass',
            name='name_ky',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='historicalproductivityclass',
            name='name_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='B01',
            field=models.TextField(blank=True, help_text='Coastal aerosol', max_length=100, null=True, verbose_name='Layer B01'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='B02',
            field=models.TextField(blank=True, help_text='Blue', max_length=100, null=True, verbose_name='Layer B02'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='B03',
            field=models.TextField(blank=True, help_text='Green', max_length=100, null=True, verbose_name='Layer B03'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='B04',
            field=models.TextField(blank=True, help_text='Red', max_length=100, null=True, verbose_name='Layer B04'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='B05',
            field=models.TextField(blank=True, help_text='Vegetation red edge', max_length=100, null=True, verbose_name='Layer B05'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='B06',
            field=models.TextField(blank=True, help_text='Vegetation red edge', max_length=100, null=True, verbose_name='Layer B06'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='B07',
            field=models.TextField(blank=True, help_text='Vegetation red edge', max_length=100, null=True, verbose_name='Layer B07'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='B08',
            field=models.TextField(blank=True, help_text='NIR', max_length=100, null=True, verbose_name='Layer B08'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='B09',
            field=models.TextField(blank=True, help_text='Water vapour', max_length=100, null=True, verbose_name='Layer B09'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='B10',
            field=models.TextField(blank=True, help_text='SWIR – Cirrus', max_length=100, null=True, verbose_name='Layer B10'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='B11',
            field=models.TextField(blank=True, help_text='SWIR – 1', max_length=100, null=True, verbose_name='Layer B11'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='B12',
            field=models.TextField(blank=True, help_text='SWIR - 2', max_length=100, null=True, verbose_name='Layer B12'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='B8A',
            field=models.TextField(blank=True, help_text='Narrow NIR', max_length=100, null=True, verbose_name='Layer B8A'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='TCI',
            field=models.TextField(blank=True, help_text='RGB', max_length=100, null=True, verbose_name='Layer TCI'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='area_interest',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='indexes.scihubareainterest', verbose_name='Area of Interest'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Image Date'),
        ),
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='polygon',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, geography='Kyrgyzstan', null=True, srid=4326, verbose_name='Image Coordinates'),
        ),
        migrations.AlterField(
            model_name='indexcreatingreport',
            name='contour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gip.contour', verbose_name='Contour'),
        ),
        migrations.AlterField(
            model_name='indexcreatingreport',
            name='is_processed',
            field=models.BooleanField(default=False, verbose_name='Being Processed'),
        ),
        migrations.AlterField(
            model_name='indexcreatingreport',
            name='process_error',
            field=models.TextField(verbose_name='Processing Errors'),
        ),
        migrations.AlterField(
            model_name='indexcreatingreport',
            name='process_error_en',
            field=models.TextField(null=True, verbose_name='Processing Errors'),
        ),
        migrations.AlterField(
            model_name='indexcreatingreport',
            name='process_error_ky',
            field=models.TextField(null=True, verbose_name='Processing Errors'),
        ),
        migrations.AlterField(
            model_name='indexcreatingreport',
            name='process_error_ru',
            field=models.TextField(null=True, verbose_name='Processing Errors'),
        ),
        migrations.AlterField(
            model_name='indexcreatingreport',
            name='satellite_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='indexes.scihubimagedate', verbose_name='Satellite Image'),
        ),
        migrations.AlterField(
            model_name='indexcreatingreport',
            name='veg_index',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='culture_model.vegetationindex', verbose_name='Vegetation Index'),
        ),
        migrations.AlterField(
            model_name='indexmeaning',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='indexmeaning',
            name='description_en',
            field=models.TextField(null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='indexmeaning',
            name='description_ky',
            field=models.TextField(null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='indexmeaning',
            name='description_ru',
            field=models.TextField(null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='indexmeaning',
            name='index',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='culture_model.vegetationindex', verbose_name='Index'),
        ),
        migrations.AlterField(
            model_name='indexmeaning',
            name='max_index_value',
            field=models.DecimalField(decimal_places=3, max_digits=4, validators=[django.core.validators.MaxValueValidator(1)], verbose_name='Maximum Value'),
        ),
        migrations.AlterField(
            model_name='indexmeaning',
            name='min_index_value',
            field=models.DecimalField(decimal_places=3, max_digits=4, validators=[django.core.validators.MinValueValidator(-1)], verbose_name='Minimum Value'),
        ),
        migrations.AlterField(
            model_name='predictedcontourvegindex',
            name='average_value',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, verbose_name='Average Index Value'),
        ),
        migrations.AlterField(
            model_name='predictedcontourvegindex',
            name='contour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contour_ai_veg_index', to='ai.contour_ai', verbose_name='Contour'),
        ),
        migrations.AlterField(
            model_name='predictedcontourvegindex',
            name='date',
            field=models.DateField(verbose_name='Analysis Date'),
        ),
        migrations.AlterField(
            model_name='predictedcontourvegindex',
            name='index',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='culture_model.vegetationindex', verbose_name='Index'),
        ),
        migrations.AlterField(
            model_name='predictedcontourvegindex',
            name='index_image',
            field=models.FileField(blank=True, upload_to='index_image', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='predictedcontourvegindex',
            name='meaning_of_average_value',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='indexes.indexmeaning', verbose_name='Index Value'),
        ),
        migrations.AlterField(
            model_name='productivityclass',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='productivityclass',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='productivityclass',
            name='description_ky',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='productivityclass',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='productivityclass',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='productivityclass',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='productivityclass',
            name='name_ky',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='productivityclass',
            name='name_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='satelliteimageband',
            name='band_description',
            field=models.TextField(verbose_name='Satellite Image Band Description'),
        ),
        migrations.AlterField(
            model_name='satelliteimageband',
            name='band_description_en',
            field=models.TextField(null=True, verbose_name='Satellite Image Band Description'),
        ),
        migrations.AlterField(
            model_name='satelliteimageband',
            name='band_description_ky',
            field=models.TextField(null=True, verbose_name='Satellite Image Band Description'),
        ),
        migrations.AlterField(
            model_name='satelliteimageband',
            name='band_description_ru',
            field=models.TextField(null=True, verbose_name='Satellite Image Band Description'),
        ),
        migrations.AlterField(
            model_name='satelliteimageband',
            name='band_name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Satellite Image Band Name'),
        ),
        migrations.AlterField(
            model_name='satelliteimageband',
            name='band_name_en',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Satellite Image Band Name'),
        ),
        migrations.AlterField(
            model_name='satelliteimageband',
            name='band_name_ky',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Satellite Image Band Name'),
        ),
        migrations.AlterField(
            model_name='satelliteimageband',
            name='band_name_ru',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Satellite Image Band Name'),
        ),
        migrations.AlterField(
            model_name='satelliteimagelayer',
            name='band',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_band', to='indexes.satelliteimageband', verbose_name='Satellite Image Band'),
        ),
        migrations.AlterField(
            model_name='satelliteimagelayer',
            name='image',
            field=models.FileField(upload_to='satellite_image', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='satelliteimagelayer',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_source', to='indexes.satelliteimagesource', verbose_name='Satellite Image Source'),
        ),
        migrations.AlterField(
            model_name='satelliteimagesource',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='satelliteimagesource',
            name='description_en',
            field=models.TextField(null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='satelliteimagesource',
            name='description_ky',
            field=models.TextField(null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='satelliteimagesource',
            name='description_ru',
            field=models.TextField(null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='satelliteimagesource',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='satelliteimagesource',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='satelliteimagesource',
            name='name_ky',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='satelliteimagesource',
            name='name_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='scihubareainterest',
            name='polygon',
            field=django.contrib.gis.db.models.fields.GeometryField(geography='Kyrgyzstan', srid=4326, verbose_name='Area of Satellite Image Interest'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='B01',
            field=models.FileField(blank=True, help_text='Coastal aerosol', null=True, upload_to='satellite_images', verbose_name='Layer B01'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='B02',
            field=models.FileField(blank=True, help_text='Blue', null=True, upload_to='satellite_images', verbose_name='Layer B02'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='B03',
            field=models.FileField(blank=True, help_text='Green', null=True, upload_to='satellite_images', verbose_name='Layer B03'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='B04',
            field=models.FileField(blank=True, help_text='Red', null=True, upload_to='satellite_images', verbose_name='Layer B04'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='B05',
            field=models.FileField(blank=True, help_text='Vegetation red edge', null=True, upload_to='satellite_images', verbose_name='Layer B05'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='B06',
            field=models.FileField(blank=True, help_text='Vegetation red edge', null=True, upload_to='satellite_images', verbose_name='Layer B06'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='B07',
            field=models.FileField(blank=True, help_text='Vegetation red edge', null=True, upload_to='satellite_images', verbose_name='Layer B07'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='B08',
            field=models.FileField(blank=True, help_text='NIR', null=True, upload_to='satellite_images', verbose_name='Layer B08'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='B09',
            field=models.FileField(blank=True, help_text='Water vapour', null=True, upload_to='satellite_images', verbose_name='Layer B09'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='B10',
            field=models.FileField(blank=True, help_text='SWIR – Cirrus', null=True, upload_to='satellite_images', verbose_name='Layer B10'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='B11',
            field=models.FileField(blank=True, help_text='SWIR – 1', null=True, upload_to='satellite_images', verbose_name='Layer B11'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='B12',
            field=models.FileField(blank=True, help_text='SWIR - 2', null=True, upload_to='satellite_images', verbose_name='Layer B12'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='B8A',
            field=models.FileField(blank=True, help_text='Narrow NIR', null=True, upload_to='satellite_images', verbose_name='Layer B8A'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='TCI',
            field=models.FileField(blank=True, help_text='RGB', null=True, upload_to='satellite_images', verbose_name='Layer TCI'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='area_interest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='image_date', to='indexes.scihubareainterest', verbose_name='Area of Interest'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Image Date'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='polygon',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, geography='Kyrgyzstan', null=True, srid=4326, verbose_name='Image Coordinates'),
        ),
    ]