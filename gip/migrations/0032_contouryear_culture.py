# Generated by Django 4.1.2 on 2023-02-28 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0031_contour_is_available_contouryear_is_available_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contouryear',
            name='culture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gip.culture'),
        ),
    ]
