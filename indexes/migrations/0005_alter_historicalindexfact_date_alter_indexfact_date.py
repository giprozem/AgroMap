# Generated by Django 4.1.2 on 2023-01-11 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexes', '0004_remove_historicalindexfact_source_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalindexfact',
            name='date',
            field=models.DateField(blank=True, verbose_name='Дата анализа'),
        ),
        migrations.AlterField(
            model_name='indexfact',
            name='date',
            field=models.DateField(blank=True, verbose_name='Дата анализа'),
        ),
    ]