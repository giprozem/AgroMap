# Generated by Django 4.1.2 on 2023-04-18 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indexes', '0033_historicalscihubimagedate_note_scihubimagedate_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalscihubimagedate',
            name='date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата снимков'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='area_interest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_date', to='indexes.scihubareainterest', verbose_name='Область интереса'),
        ),
        migrations.AlterField(
            model_name='scihubimagedate',
            name='date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата снимков'),
        ),
    ]