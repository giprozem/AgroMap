# Generated by Django 4.1.2 on 2023-02-22 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0024_alter_farmer_options_alter_fertility_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicallanduse',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Land use', 'verbose_name_plural': 'historical Land use'},
        ),
        migrations.AlterModelOptions(
            name='historicallandusephotos',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Land use photo', 'verbose_name_plural': 'historical Land use photos'},
        ),
        migrations.AlterModelOptions(
            name='historicalorthophoto',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Satellite image', 'verbose_name_plural': 'historical Satellite RGB'},
        ),
        migrations.AlterModelOptions(
            name='landuse',
            options={'verbose_name': 'Land use', 'verbose_name_plural': 'Land use'},
        ),
        migrations.AlterModelOptions(
            name='landusephotos',
            options={'verbose_name': 'Land use photo', 'verbose_name_plural': 'Land use photos'},
        ),
        migrations.AlterModelOptions(
            name='orthophoto',
            options={'verbose_name': 'Satellite image', 'verbose_name_plural': 'Satellite RGB'},
        ),
        migrations.AddField(
            model_name='orthophoto',
            name='layer_name_en',
            field=models.CharField(max_length=55, null=True, verbose_name='Layer name'),
        ),
        migrations.AddField(
            model_name='orthophoto',
            name='layer_name_ky',
            field=models.CharField(max_length=55, null=True, verbose_name='Layer name'),
        ),
        migrations.AddField(
            model_name='orthophoto',
            name='layer_name_ru',
            field=models.CharField(max_length=55, null=True, verbose_name='Layer name'),
        ),
        migrations.AlterField(
            model_name='historicallanduse',
            name='contour',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.contour', verbose_name='Field'),
        ),
        migrations.AlterField(
            model_name='historicallanduse',
            name='culture',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.culture', verbose_name='Culture'),
        ),
        migrations.AlterField(
            model_name='historicallanduse',
            name='farmer',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.farmer', verbose_name='Farmer'),
        ),
        migrations.AlterField(
            model_name='historicallanduse',
            name='season',
            field=models.IntegerField(blank=True, null=True, verbose_name='Season'),
        ),
        migrations.AlterField(
            model_name='historicallanduse',
            name='year',
            field=models.IntegerField(verbose_name='Year'),
        ),
        migrations.AlterField(
            model_name='historicalorthophoto',
            name='file',
            field=models.TextField(max_length=100, verbose_name='Satellite image'),
        ),
        migrations.AlterField(
            model_name='historicalorthophoto',
            name='layer_name',
            field=models.CharField(max_length=55, verbose_name='Layer name'),
        ),
        migrations.AlterField(
            model_name='historicalorthophoto',
            name='url',
            field=models.URLField(max_length=1024, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='historicalorthophoto',
            name='use_y_n',
            field=models.BooleanField(verbose_name='Use'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='contour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='land_uses', to='gip.contour', verbose_name='Field'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='culture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='land_uses', to='gip.culture', verbose_name='Culture'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='farmer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='land_uses', to='gip.farmer', verbose_name='Farmer'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='season',
            field=models.IntegerField(blank=True, null=True, verbose_name='Season'),
        ),
        migrations.AlterField(
            model_name='landuse',
            name='year',
            field=models.IntegerField(verbose_name='Year'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='file',
            field=models.FileField(upload_to='ortho_photo', verbose_name='Satellite image'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='layer_name',
            field=models.CharField(max_length=55, verbose_name='Layer name'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='url',
            field=models.URLField(max_length=1024, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='orthophoto',
            name='use_y_n',
            field=models.BooleanField(verbose_name='Use'),
        ),
    ]
