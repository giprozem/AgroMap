# Generated by Django 4.1.2 on 2023-11-22 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0072_delete_elevation'),
    ]

    operations = [
        migrations.AddField(
            model_name='contour',
            name='cadastre',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalcontour',
            name='cadastre',
            field=models.BooleanField(default=False),
        ),
    ]