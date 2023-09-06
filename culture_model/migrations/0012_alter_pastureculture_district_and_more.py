# Generated by Django 4.1.2 on 2023-08-17 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0060_conton_code_soato_vet_district_code_soato_vet_and_more'),
        ('culture_model', '0011_remove_pastureculture_culture_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pastureculture',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gip.district', verbose_name='Район'),
        ),
        migrations.AlterField(
            model_name='pastureculture',
            name='veg_period',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='culture_model.phase', verbose_name='Вегетационный период'),
        ),
    ]