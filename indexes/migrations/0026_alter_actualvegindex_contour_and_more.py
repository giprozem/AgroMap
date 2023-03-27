# Generated by Django 4.1.2 on 2023-03-16 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0043_remove_contouryear_contour_and_more'),
        ('indexes', '0025_alter_indexcreatingreport_veg_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actualvegindex',
            name='contour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actual_veg_index', to='gip.contour', verbose_name='Контуры поля'),
        ),
        migrations.AlterField(
            model_name='contouraverageindex',
            name='contour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gip.contour', verbose_name='Контуры поля'),
        ),
        migrations.AlterField(
            model_name='historicalactualvegindex',
            name='contour',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.contour', verbose_name='Контуры поля'),
        ),
        migrations.AlterField(
            model_name='historicalcontouraverageindex',
            name='contour',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.contour', verbose_name='Контуры поля'),
        ),
        migrations.AlterField(
            model_name='indexcreatingreport',
            name='contour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gip.contour', verbose_name='Контур'),
        ),
    ]