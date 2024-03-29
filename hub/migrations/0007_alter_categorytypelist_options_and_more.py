# Generated by Django 4.1.2 on 2023-09-23 07:53

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0006_alter_historicallandinfo_crmid_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorytypelist',
            options={'verbose_name': 'Land Categories', 'verbose_name_plural': 'Land Categories'},
        ),
        migrations.AlterModelOptions(
            name='documenttypelist',
            options={'verbose_name': 'Legal Documents', 'verbose_name_plural': 'Legal Documents'},
        ),
        migrations.AlterModelOptions(
            name='historicallandinfo',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'History', 'verbose_name_plural': 'historical Main Table'},
        ),
        migrations.AlterModelOptions(
            name='landinfo',
            options={'verbose_name': 'Main Table', 'verbose_name_plural': 'Main Table'},
        ),
        migrations.AlterModelOptions(
            name='landtypelist',
            options={'verbose_name': 'Land Types Data', 'verbose_name_plural': 'Land Types Data'},
        ),
        migrations.AlterModelOptions(
            name='propertytypelist',
            options={'verbose_name': 'Property Type Data', 'verbose_name_plural': 'Property Type Data'},
        ),
        migrations.AlterField(
            model_name='categorytypelist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation Date'),
        ),
        migrations.AlterField(
            model_name='categorytypelist',
            name='type_name',
            field=models.CharField(max_length=50, verbose_name='Category Name'),
        ),
        migrations.AlterField(
            model_name='categorytypelist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='documenttypelist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation Date'),
        ),
        migrations.AlterField(
            model_name='documenttypelist',
            name='type_name',
            field=models.CharField(max_length=50, verbose_name='Document Name'),
        ),
        migrations.AlterField(
            model_name='documenttypelist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='agro_type_land',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Agricultural Land Type'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='agroland_purposes',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Agricultural Land Purposes'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='asr_address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Parcel Address (ASR)'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='bonitet',
            field=models.IntegerField(blank=True, null=True, verbose_name='Bonniness'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='category_type',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='hub.categorytypelist', verbose_name='Land Categories'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='certifying_act',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Certifying Act (Attach File)'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='circuit_number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Circuit Number'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='collective_gardens_and_veg',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Collective Gardens and Vegetable Plots'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Creation Date'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='crmid',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Identification Number'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='crop_yield',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True, verbose_name='Crop Yield'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='culture',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Crop Type'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='date_of_completion',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Completion Date'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='desc_brd',
            field=models.TextField(blank=True, null=True, verbose_name='Description of Restrictions'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='descriptiom_doc',
            field=models.TextField(blank=True, null=True, verbose_name='Description (if needed)'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='description',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='disturbed_lands',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Disturbed Lands'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='doc_enttitlement',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Document Entitlement'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='document_link',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Document Link'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='document_type',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='hub.documenttypelist', verbose_name='Document Type'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='elementary_sectionnumber',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Elementary Section Number'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='eni_code',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='ENI Code'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='forest_areas',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Forest Areas'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='form_using_asr',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Use Form (ASR)'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='gfsu',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='State Fund of Agricultural Lands'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='haushold_land',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Household Lands and Citizen Allotments'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='improved_radical',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Improved (Radical Improvement)'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='inaccessible',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Inaccessible Due to Difficulty of Access'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='ink_code',
            field=models.CharField(max_length=100, verbose_name='INK Code'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='inn_pin',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tax ID'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='intensive_use',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Intensive Use'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='irrigated',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Irrigated'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='land_ctg',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Land Categories (Land Balance)'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='land_factarea_asr',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Actual Area (ASR)'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='land_legalarea',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Legal Area (ASR)'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='land_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Land Number'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='land_type',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='hub.landtypelist', verbose_name='Land Type Information'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='lands_pop_areas',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Lands in Populated Areas'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='latitude',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='limite',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Limitations'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='longitude',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='lot_number',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Lot Number'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='main_map',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326, verbose_name='Contour'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='modifiedby',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Modified By'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='number_of_families',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Number of Families'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='number_of_yards',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Number of Yards'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='number_realestateunits',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Number of Real Estate Units'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='otherlands',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Other Lands'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='othertypes_lands',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Other Types of Lands'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='owner_info',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Owner Information (ASR)'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='pasture',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Pasture'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='perrenial_plant',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Perennial Plants'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='plant_not_forestfund',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Non-Forest Fund Woody and Shrub Plantations'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='property_form',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Property Form'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='property_type',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='hub.propertytypelist', verbose_name='Property Type'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='rainfed',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Rainfed'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='setype',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='smcreatorid',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Creator'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='smownerid',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='special_purpose_asr',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Special Purpose (ASR)'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='square',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True, verbose_name='Actual Area'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='status',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='territorial_outline',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Administrative-Territorial Division'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='total_land',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Total Land'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='type_of_land',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Land Types'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='udp',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Long-Term Land Use'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='underwater',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Underwater'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='use_end',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Use End Date'),
        ),
        migrations.AlterField(
            model_name='historicallandinfo',
            name='use_period',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Use Period (Years)'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='agro_type_land',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Agricultural Land Type'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='agroland_purposes',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Agricultural Land Purposes'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='asr_address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Parcel Address (ASR)'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='bonitet',
            field=models.IntegerField(blank=True, null=True, verbose_name='Bonniness'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='category_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='land_info', to='hub.categorytypelist', verbose_name='Land Categories'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='certifying_act',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Certifying Act (Attach File)'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='circuit_number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Circuit Number'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='collective_gardens_and_veg',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Collective Gardens and Vegetable Plots'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation Date'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='crmid',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Identification Number'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='crop_yield',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True, verbose_name='Crop Yield'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='culture',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Crop Type'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='date_of_completion',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Completion Date'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='desc_brd',
            field=models.TextField(blank=True, null=True, verbose_name='Description of Restrictions'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='descriptiom_doc',
            field=models.TextField(blank=True, null=True, verbose_name='Description (if needed)'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='description',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='disturbed_lands',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Disturbed Lands'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='doc_enttitlement',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Document Entitlement'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='document_link',
            field=models.FileField(blank=True, null=True, upload_to='document', verbose_name='Document Link'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='document_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='land_info', to='hub.documenttypelist', verbose_name='Document Type'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='elementary_sectionnumber',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Elementary Section Number'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='eni_code',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='ENI Code'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='forest_areas',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Forest Areas'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='form_using_asr',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Use Form (ASR)'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='gfsu',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='State Fund of Agricultural Lands'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='haushold_land',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Household Lands and Citizen Allotments'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='improved_radical',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Improved (Radical Improvement)'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='inaccessible',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Inaccessible Due to Difficulty of Access'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='ink_code',
            field=models.CharField(max_length=100, verbose_name='INK Code'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='inn_pin',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tax ID'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='intensive_use',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Intensive Use'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='irrigated',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Irrigated'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='land_ctg',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Land Categories (Land Balance)'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='land_factarea_asr',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Actual Area (ASR)'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='land_legalarea',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Legal Area (ASR)'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='land_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Land Number'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='land_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='land_info', to='hub.landtypelist', verbose_name='Land Type Information'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='lands_pop_areas',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Lands in Populated Areas'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='latitude',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='limite',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Limitations'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='longitude',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='lot_number',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Lot Number'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='main_map',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326, verbose_name='Contour'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='modifiedby',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Modified By'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='number_of_families',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Number of Families'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='number_of_yards',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Number of Yards'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='number_realestateunits',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Number of Real Estate Units'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='otherlands',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Other Lands'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='othertypes_lands',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Other Types of Lands'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='owner_info',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Owner Information (ASR)'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='pasture',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Pasture'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='perrenial_plant',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Perennial Plants'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='plant_not_forestfund',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Non-Forest Fund Woody and Shrub Plantations'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='property_form',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Property Form'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='property_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='land_info', to='hub.propertytypelist', verbose_name='Property Type'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='rainfed',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Rainfed'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='setype',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='smcreatorid',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Creator'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='smownerid',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='special_purpose_asr',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Special Purpose (ASR)'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='square',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True, verbose_name='Actual Area'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='status',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='territorial_outline',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Administrative-Territorial Division'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='total_land',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Total Land'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='type_of_land',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Land Types'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='udp',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Long-Term Land Use'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='underwater',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Underwater'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='use_end',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Use End Date'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='use_period',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Use Period (Years)'),
        ),
        migrations.AlterField(
            model_name='landtypelist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation Date'),
        ),
        migrations.AlterField(
            model_name='landtypelist',
            name='type_name',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='landtypelist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update Date'),
        ),
        migrations.AlterField(
            model_name='propertytypelist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation Date'),
        ),
        migrations.AlterField(
            model_name='propertytypelist',
            name='type_name',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='propertytypelist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update Date'),
        ),
    ]
