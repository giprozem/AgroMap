# Generated by Django 4.1.2 on 2023-08-17 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('culture_model', '0012_alter_pastureculture_district_and_more'),
        ('gip', '0060_conton_code_soato_vet_district_code_soato_vet_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contour',
            name='pasture_culture',
            field=models.ManyToManyField(blank=True, default=None, help_text='Required if land type is pasture', to='culture_model.pastureculture', verbose_name='Культура пастбища'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='predicted_productivity',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Прогнозируемая родуктивность'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='predicted_productivity',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Прогнозируемая родуктивность'),
        ),
    ]