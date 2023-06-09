# Generated by Django 4.1.2 on 2023-02-07 10:36

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0015_conton_code_soato_district_code_soato_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contour',
            name='area_ha',
        ),
        migrations.RemoveField(
            model_name='contour',
            name='polygon',
        ),
        migrations.RemoveField(
            model_name='contour',
            name='type',
        ),
        migrations.RemoveField(
            model_name='historicalcontour',
            name='area_ha',
        ),
        migrations.RemoveField(
            model_name='historicalcontour',
            name='polygon',
        ),
        migrations.RemoveField(
            model_name='historicalcontour',
            name='type',
        ),
        migrations.AddField(
            model_name='contour',
            name='code_soato',
            field=models.CharField(max_length=30, null=True, unique=True, verbose_name='Код СОАТО'),
        ),
        migrations.AddField(
            model_name='historicalcontour',
            name='code_soato',
            field=models.CharField(db_index=True, max_length=30, null=True, verbose_name='Код СОАТО'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='farmer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contours', to='gip.farmer', verbose_name='Фермер'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='ink',
            field=models.CharField(blank=True, help_text='Идентификационный Номер Контура', max_length=100, null=True, unique=True, verbose_name='ИНК'),
        ),
        migrations.AlterField(
            model_name='contour',
            name='is_rounded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='ink',
            field=models.CharField(blank=True, db_index=True, help_text='Идентификационный Номер Контура', max_length=100, null=True, verbose_name='ИНК'),
        ),
        migrations.AlterField(
            model_name='historicalcontour',
            name='is_rounded',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ContourYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('code_soato', models.CharField(max_length=30, null=True, unique=True, verbose_name='Код СОАТО')),
                ('polygon', django.contrib.gis.db.models.fields.GeometryField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур')),
                ('year', models.CharField(max_length=20)),
                ('productivity', models.CharField(blank=True, max_length=20, null=True)),
                ('area_ha', models.FloatField(blank=True, null=True, verbose_name='Площадь га')),
                ('contour', models.ManyToManyField(to='gip.contour', verbose_name='Контуры полей')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contours', to='gip.landtype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
