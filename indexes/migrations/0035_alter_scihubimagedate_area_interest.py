# Generated by Django 4.1.2 on 2023-04-19 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indexes', '0034_alter_historicalscihubimagedate_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scihubimagedate',
            name='area_interest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='image_date', to='indexes.scihubareainterest', verbose_name='Область интереса'),
        ),
    ]
