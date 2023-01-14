# Generated by Django 4.1.2 on 2023-01-11 09:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexes', '0002_remove_historicalindexfact_decade_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalindexfact',
            name='date',
            field=models.DateField(default=datetime.date(2022, 3, 4), verbose_name='Дата анализа'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='indexfact',
            name='date',
            field=models.DateField(default=datetime.date(2022, 3, 4), verbose_name='Дата анализа'),
            preserve_default=False,
        ),
    ]