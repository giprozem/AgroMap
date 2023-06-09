# Generated by Django 4.1.2 on 2022-11-28 12:39

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gip', '0006_alter_conton_options_alter_contour_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contour',
            options={'verbose_name': 'Контуры Поля', 'verbose_name_plural': 'Контуры полей'},
        ),
        migrations.AlterModelOptions(
            name='historicalcontour',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'История', 'verbose_name_plural': 'historical Контуры полей'},
        ),
        migrations.RemoveField(
            model_name='conton',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='conton',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='contour',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='contour',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='cropyield',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='cropyield',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='culture',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='culture',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='district',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='district',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='farmer',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='farmer',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='fertility',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='fertility',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='historicalconton',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='historicalconton',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='historicalcontour',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='historicalcontour',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='historicalcropyield',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='historicalcropyield',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='landuse',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='landuse',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='landusephotos',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='landusephotos',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='orthophoto',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='orthophoto',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='region',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='region',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='soilclass',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='soilclass',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='soilclassmap',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='soilclassmap',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='soilfertility',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='soilfertility',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='soilproductivity',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='soilproductivity',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='village',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='village',
            name='updated_by',
        ),
        migrations.CreateModel(
            name='HistoricalVillage',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='время обновления')),
                ('name', models.CharField(max_length=55, verbose_name='Село')),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('conton', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.conton', verbose_name='Район')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Село',
                'verbose_name_plural': 'historical Сёла',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSoilProductivity',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='время обновления')),
                ('name', models.CharField(max_length=255, verbose_name='Продуктивность почвы')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Продуктивность почвы',
                'verbose_name_plural': 'historical Продуктивность почв',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSoilFertility',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='время обновления')),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('soil_productivity', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.soilproductivity', verbose_name='Продуктивность почвы')),
            ],
            options={
                'verbose_name': 'historical Плодородие почвы',
                'verbose_name_plural': 'historical Плодородие почв',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSoilClassMap',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='время обновления')),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('soil_class', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.soilclass', verbose_name='Вид почвы')),
            ],
            options={
                'verbose_name': 'historical Контур вида почвы',
                'verbose_name_plural': 'historical Контуры вида почвы',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSoilClass',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='время обновления')),
                ('name', models.CharField(max_length=55, verbose_name='Вид почвы')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('fertility', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.fertility', verbose_name='Название удобрение')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Вид почвы',
                'verbose_name_plural': 'historical Виды почв',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalRegion',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='время обновления')),
                ('name', models.CharField(max_length=55, verbose_name='Наименование области')),
                ('population', models.IntegerField(verbose_name='Население')),
                ('area', models.IntegerField(verbose_name='Площадь')),
                ('density', models.FloatField(verbose_name='Плотность')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Область',
                'verbose_name_plural': 'historical Области',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalOrthoPhoto',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='время обновления')),
                ('layer_name', models.CharField(max_length=55, verbose_name='Название слоя')),
                ('url', models.URLField(max_length=1024, verbose_name='Ссылка')),
                ('use_y_n', models.BooleanField(verbose_name='Использовать')),
                ('file', models.TextField(max_length=100, verbose_name='Спутниковый снимок')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Спутниковый снимок',
                'verbose_name_plural': 'historical Спутниковые снимки',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalLandUsePhotos',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='время обновления')),
                ('image', models.TextField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('land_use', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.landuse')),
            ],
            options={
                'verbose_name': 'historical Фото землепользования',
                'verbose_name_plural': 'historical Фото земепользования',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalLandUse',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='время обновления')),
                ('year', models.IntegerField(verbose_name='Год')),
                ('season', models.IntegerField(blank=True, null=True, verbose_name='Сезон')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('contour', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.contour', verbose_name='Поле')),
                ('culture', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.culture', verbose_name='Культура')),
                ('farmer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.farmer', verbose_name='Фермер')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Землепользование',
                'verbose_name_plural': 'historical Земепользования',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalFertility',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='время обновления')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование удобрения')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Удобрение',
                'verbose_name_plural': 'historical Удобрения',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalFarmer',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='время обновления')),
                ('pin_inn', models.CharField(max_length=14, verbose_name='ПИН или ИНН')),
                ('mobile', models.CharField(max_length=20, verbose_name='номер телефона')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Фермер')),
            ],
            options={
                'verbose_name': 'historical Фермер',
                'verbose_name_plural': 'historical Фермеры',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalDistrict',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='время обновления')),
                ('name', models.CharField(max_length=55, verbose_name='Район')),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(geography='Kyrgyzstan', srid=4326, verbose_name='Контур')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('region', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gip.region', verbose_name='Область')),
            ],
            options={
                'verbose_name': 'historical Район',
                'verbose_name_plural': 'historical Район',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCulture',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='время обновления')),
                ('name', models.CharField(max_length=55, verbose_name='Культура')),
                ('coefficient_crop', models.FloatField(verbose_name='Коеффициент урожайности')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Культура',
                'verbose_name_plural': 'historical Культуры',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
