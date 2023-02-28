# Generated by Django 4.1.2 on 2023-02-28 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gip', '0030_alter_conton_options_alter_contour_options_and_more'),
        ('culture_model', '0004_alter_decade_options_alter_indexplan_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='decade',
            options={'verbose_name': 'Декада', 'verbose_name_plural': 'Декады'},
        ),
        migrations.AlterModelOptions(
            name='indexplan',
            options={'verbose_name': 'Плановое значение индекса', 'verbose_name_plural': 'Плановые значения индекса'},
        ),
        migrations.AlterModelOptions(
            name='phase',
            options={'verbose_name': 'Фаза развития', 'verbose_name_plural': 'Фазы развития'},
        ),
        migrations.AlterModelOptions(
            name='vegetationindex',
            options={'verbose_name': 'Индекс', 'verbose_name_plural': 'Индексы'},
        ),
        migrations.AlterField(
            model_name='decade',
            name='end_date',
            field=models.DateField(verbose_name='До'),
        ),
        migrations.AlterField(
            model_name='decade',
            name='start_date',
            field=models.DateField(verbose_name='С'),
        ),
        migrations.AlterField(
            model_name='indexplan',
            name='culture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='index_plans', to='gip.culture', verbose_name='Культура'),
        ),
        migrations.AlterField(
            model_name='indexplan',
            name='decade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='index_plans', to='culture_model.decade', verbose_name='Декада'),
        ),
        migrations.AlterField(
            model_name='indexplan',
            name='index',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='index_plans', to='culture_model.vegetationindex', verbose_name='Индекс'),
        ),
        migrations.AlterField(
            model_name='indexplan',
            name='phase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='index_plans', to='culture_model.phase', verbose_name='Фаза'),
        ),
        migrations.AlterField(
            model_name='indexplan',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='index_plans', to='gip.region', verbose_name='Область'),
        ),
        migrations.AlterField(
            model_name='indexplan',
            name='value',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5, verbose_name='Значение индекса'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='name',
            field=models.CharField(max_length=125, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='name_en',
            field=models.CharField(max_length=125, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='name_ky',
            field=models.CharField(max_length=125, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='name_ru',
            field=models.CharField(max_length=125, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='vegetationindex',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='vegetationindex',
            name='description_en',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='vegetationindex',
            name='description_ky',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='vegetationindex',
            name='description_ru',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='vegetationindex',
            name='name',
            field=models.CharField(max_length=125, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='vegetationindex',
            name='name_en',
            field=models.CharField(max_length=125, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='vegetationindex',
            name='name_ky',
            field=models.CharField(max_length=125, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='vegetationindex',
            name='name_ru',
            field=models.CharField(max_length=125, null=True, verbose_name='Название'),
        ),
    ]
