# Generated by Django 4.1.2 on 2023-10-04 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0070_culturetype_name_en_culturetype_name_ky_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contour',
            name='conton',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contours', to='gip.conton', verbose_name='Conton'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='coefficient_crop',
            field=models.FloatField(default=0.0, verbose_name='Crop Productivity Coefficient'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='culture_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='culture_id', to='gip.culturetype', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Culture'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='name_en',
            field=models.CharField(max_length=55, null=True, verbose_name='Culture'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='name_ky',
            field=models.CharField(max_length=55, null=True, verbose_name='Culture'),
        ),
        migrations.AlterField(
            model_name='culture',
            name='name_ru',
            field=models.CharField(max_length=55, null=True, verbose_name='Culture'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='conton',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.conton', verbose_name='Conton'),
        ),
        migrations.AlterField(
            model_name='historicalculture',
            name='coefficient_crop',
            field=models.FloatField(default=0.0, verbose_name='Crop Productivity Coefficient'),
        ),
        migrations.AlterField(
            model_name='historicalculture',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Culture'),
        ),
        migrations.AlterField(
            model_name='historicalculture',
            name='name_en',
            field=models.CharField(max_length=55, null=True, verbose_name='Culture'),
        ),
        migrations.AlterField(
            model_name='historicalculture',
            name='name_ky',
            field=models.CharField(max_length=55, null=True, verbose_name='Culture'),
        ),
        migrations.AlterField(
            model_name='historicalculture',
            name='name_ru',
            field=models.CharField(max_length=55, null=True, verbose_name='Culture'),
        ),
    ]