# Generated by Django 4.1.2 on 2023-04-18 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexes', '0031_historicalscihubimagedate_image_png_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalscihubimagedate',
            name='no_image',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='scihubimagedate',
            name='no_image',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
