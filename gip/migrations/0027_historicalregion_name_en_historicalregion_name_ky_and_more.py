# Generated by Django 4.1.2 on 2023-02-23 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0026_alter_historicalregion_options_alter_region_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalregion',
            name='name_en',
            field=models.CharField(max_length=55, null=True, verbose_name='Region name'),
        ),
        migrations.AddField(
            model_name='historicalregion',
            name='name_ky',
            field=models.CharField(max_length=55, null=True, verbose_name='Region name'),
        ),
        migrations.AddField(
            model_name='historicalregion',
            name='name_ru',
            field=models.CharField(max_length=55, null=True, verbose_name='Region name'),
        ),
    ]
