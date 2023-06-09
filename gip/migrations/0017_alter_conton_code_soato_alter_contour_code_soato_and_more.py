# Generated by Django 4.1.2 on 2023-02-07 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0016_remove_contour_area_ha_remove_contour_polygon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conton',
            name='code_soato',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Код СОАТО'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='code_soato',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Код СОАТО'),
        ),
        migrations.AlterField(
            model_name='contouryear',
            name='code_soato',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Код СОАТО'),
        ),
        migrations.AlterField(
            model_name='district',
            name='code_soato',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Код СОАТО'),
        ),
        migrations.AlterField(
            model_name='historicalconton',
            name='code_soato',
            field=models.CharField(blank=True, db_index=True, max_length=30, null=True, verbose_name='Код СОАТО'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='code_soato',
            field=models.CharField(blank=True, db_index=True, max_length=30, null=True, verbose_name='Код СОАТО'),
        ),
        migrations.AlterField(
            model_name='historicaldistrict',
            name='code_soato',
            field=models.CharField(blank=True, db_index=True, max_length=30, null=True, verbose_name='Код СОАТО'),
        ),
        migrations.AlterField(
            model_name='historicalregion',
            name='code_soato',
            field=models.CharField(blank=True, db_index=True, max_length=30, null=True, verbose_name='Код СОАТО'),
        ),
        migrations.AlterField(
            model_name='region',
            name='code_soato',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Код СОАТО'),
        ),
    ]
