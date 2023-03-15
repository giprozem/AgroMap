# Generated by Django 4.1.2 on 2023-03-15 12:52

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gip', '0041_contouryear_elevation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='elevation',
            options={'verbose_name': 'Высота', 'verbose_name_plural': 'Высоты'},
        ),
        migrations.AlterField(
            model_name='contouryear',
            name='elevation',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Высота'),
        ),
        migrations.AlterField(
            model_name='elevation',
            name='elevation',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Высота'),
        ),
        migrations.CreateModel(
            name='HistoricalContourYear',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Дата обновления')),
                ('code_soato', models.CharField(blank=True, db_index=True, max_length=30, null=True, verbose_name='Код СОАТО')),
                ('polygon', django.contrib.gis.db.models.fields.GeometryField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур')),
                ('year', models.CharField(max_length=20, verbose_name='Год')),
                ('productivity', models.CharField(blank=True, max_length=20, null=True, verbose_name='Продуктивность')),
                ('area_ha', models.FloatField(blank=True, null=True, verbose_name='Площадь в гектарах')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удаленный')),
                ('elevation', models.CharField(blank=True, max_length=25, null=True, verbose_name='Высота')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('contour', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.contour', verbose_name='Контуры полей')),
                ('culture', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.culture', verbose_name='Культура')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('type', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.landtype', verbose_name='Тип земли')),
            ],
            options={
                'verbose_name': 'История',
                'verbose_name_plural': 'historical Контуры полей по годам',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
