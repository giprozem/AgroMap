# Generated by Django 4.1.2 on 2023-02-17 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('culture_model', '0003_rename_index_vegetationindex'),
        ('gip', '0019_alter_contouryear_contour_alter_contouryear_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('indexes', '0017_alter_contouraverageindex_contour_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActualVegIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_image', models.FileField(blank=True, upload_to='index_image', verbose_name='Картинка индекса')),
                ('average_value', models.DecimalField(blank=True, decimal_places=3, max_digits=5, verbose_name='Средий показатель индекса')),
                ('date', models.DateField(help_text='Введите дату космо снимка из которого будет высчитан индекс', verbose_name='Дата анализа')),
                ('contour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actual_veg_index', to='gip.contouryear', verbose_name='Контуры Поля')),
                ('index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='culture_model.vegetationindex', verbose_name='Индекс')),
                ('meaning_of_average_value', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='indexes.indexmeaning', verbose_name='Значение среднего показателя')),
            ],
            options={
                'verbose_name': 'Фактический Индекс',
                'verbose_name_plural': 'Фактические Индексы',
            },
        ),
        migrations.RenameModel(
            old_name='HistoricalActuaVegIndex',
            new_name='HistoricalActualVegIndex',
        ),
        migrations.DeleteModel(
            name='ActuaVegIndex',
        ),
    ]