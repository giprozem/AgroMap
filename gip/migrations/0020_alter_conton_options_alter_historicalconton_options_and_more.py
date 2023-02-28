# Generated by Django 4.1.2 on 2023-02-22 05:50

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0019_alter_contouryear_contour_alter_contouryear_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conton',
            options={'verbose_name': 'Aiyl aimag', 'verbose_name_plural': 'Aiyl aimags'},
        ),
        migrations.AlterModelOptions(
            name='historicalconton',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'History', 'verbose_name_plural': 'historical Aiyl aimags'},
        ),
        migrations.AddField(
            model_name='conton',
            name='name_en',
            field=models.CharField(max_length=55, null=True, verbose_name='Aiyl aimag name'),
        ),
        migrations.AddField(
            model_name='conton',
            name='name_ky',
            field=models.CharField(max_length=55, null=True, verbose_name='Aiyl aimag name'),
        ),
        migrations.AddField(
            model_name='conton',
            name='name_ru',
            field=models.CharField(max_length=55, null=True, verbose_name='Aiyl aimag name'),
        ),
        migrations.AlterField(
            model_name='conton',
            name='code_soato',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='SOATO code'),
        ),
        migrations.AlterField(
            model_name='conton',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='conton',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contons', to='gip.district', verbose_name='District'),
        ),
        migrations.AlterField(
            model_name='conton',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Aiyl aimag name'),
        ),
        migrations.AlterField(
            model_name='conton',
            name='polygon',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, geography='Kyrgyzstan', null=True, srid=4326, verbose_name='Polygon'),
        ),
        migrations.AlterField(
            model_name='conton',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='contouryear',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='contouryear',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='cropyield',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='cropyield',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='district',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='district',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='fertility',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='fertility',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='code_soato',
            field=models.CharField(blank=True, db_index=True, max_length=30, null=True, verbose_name='SOATO code'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='district',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.district', verbose_name='District'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Aiyl aimag name'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='polygon',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, geography='Kyrgyzstan', null=True, srid=4326, verbose_name='Polygon'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicalcropyield',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicalcropyield',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicalculture',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicalculture',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicaldistrict',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicaldistrict',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicalfarmer',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicalfarmer',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicalfertility',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicalfertility',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicallanduse',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicallanduse',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicallandusephotos',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicallandusephotos',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicalorthophoto',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicalorthophoto',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicalregion',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicalregion',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicalsoilclass',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicalsoilclass',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicalsoilclassmap',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicalsoilclassmap',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicalsoilfertility',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicalsoilfertility',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicalsoilproductivity',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicalsoilproductivity',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='historicalvillage',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='historicalvillage',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='landusephotos',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='landusephotos',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='region',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='region',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='soilclass',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='soilclass',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='soilclassmap',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='soilclassmap',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='soilfertility',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='soilfertility',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='soilproductivity',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='soilproductivity',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
        migrations.AlterField(
            model_name='village',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='village',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Update time'),
        ),
    ]