# Generated by Django 4.1.2 on 2023-06-21 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0055_delete_fertility_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contour',
            name='eni',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='ЕНИ'),
        ),
        migrations.AddField(
            model_name='historicalcontour',
            name='eni',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='ЕНИ'),
        ),
    ]