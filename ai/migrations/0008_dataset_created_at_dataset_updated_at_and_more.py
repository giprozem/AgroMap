# Generated by Django 4.1.2 on 2023-04-05 07:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0049_remove_culture_fill_color_and_more'),
        ('ai', '0007_dataset'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataset',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='contour_ai',
            name='culture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gip.culture', verbose_name='Культура'),
        ),
    ]
