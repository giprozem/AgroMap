# Generated by Django 4.1.2 on 2023-03-16 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0044_delete_contouryear_delete_historicalcontouryear'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contour',
            name='ink',
            field=models.CharField(blank=True, help_text='Идентификационный номер контура', max_length=100, null=True, verbose_name='ИНК'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='ink',
            field=models.CharField(blank=True, help_text='Идентификационный номер контура', max_length=100, null=True, verbose_name='ИНК'),
        ),
    ]
